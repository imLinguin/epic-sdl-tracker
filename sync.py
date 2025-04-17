#!/usr/bin/python3

import chunk as legendary_chunk
import manifest as legendary_manifest
import requests
import logging
import shutil
import os

logging.basicConfig(level=logging.DEBUG)

session = requests.session()
session.headers['User-Agent'] = 'EpicGamesLauncher/11.0.1-14907503+++Portal+Release-Live Windows/10.0.19041.1.256.64bit'

response = session.post("https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                        data={
                            "grant_type": "client_credentials",
                            "token_type": "eg1"
                            },
            headers={
                "Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="
                })

tokens = response.json()

token = tokens["access_token"]

response = session.get(f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/Windows/launcher?label=Live-Interceptor", headers={
    "Authorization": f"bearer {token}"
    })

update_data = response.json()

elements = update_data["elements"]

for element in elements:
    if element["appName"] == "EpicGamesLauncher":
        if "GITHUB_OUTPUT" in os.environ:
            open(os.environ["GITHUB_OUTPUT"], 'a').write("epicversion=" + element["buildVersion"] + "\n")

        manifests = element["manifests"]
        manifest = manifests[0]
        base_url = manifest["uri"].rsplit("/", 1)[0]
        response = session.get(manifest["uri"], params={param["name"]: param["value"] for param in manifest["queryParams"]})

        mfst = legendary_manifest.Manifest.read_all(response.content)

        os.makedirs("sdls-temp", exist_ok=True)
        # Get chunks
        chunk_cache = dict()
        for file in mfst.file_manifest_list.elements:
            if not file.filename.endswith("sdmeta"):
                continue
            for part in file.chunk_parts:
                if part.guid in chunk_cache:
                    continue
                chunk = mfst.chunk_data_list.get_chunk_by_guid(part.guid_str)
                resp = session.get(base_url+"/"+chunk.path)
                chunk_data = legendary_chunk.Chunk.read_buffer(resp.content)
                chunk_cache[chunk.guid] = chunk_data

        # Write files
        for file in mfst.file_manifest_list.elements:
            if not file.filename.endswith("sdmeta"):
                continue
            with open("sdls-temp/" + file.filename.rsplit('/', 1)[1], 'wb') as f:
                for part in file.chunk_parts:
                    chunk_data = chunk_cache[part.guid]
                    f.write(chunk_data.data[part.offset:part.offset+part.size])

shutil.rmtree("sdls", ignore_errors=True)
os.rename("sdls-temp", "sdls")
