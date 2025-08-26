# Epic SelectiveDL tracker

[![Synchronize](https://github.com/imLinguin/epic-sdl-tracker/actions/workflows/sync.yml/badge.svg)](https://github.com/imLinguin/epic-sdl-tracker/actions/workflows/sync.yml)

This repository automatically synchronizes latest SelectiveDL manifests used by EpicGamesLauncher to filter downloaded files based on given inputs.

## How does it work?

The automation uses EpicGamesLauncher's update system to pull latest  `.v#sdmeta` files.

## Parsing manifests

Manifests are JSON files that describe a set of tags that correspond to given selections that should be exposed to the user.   
Most structures make use of Unreal Engine expressions for matching game versions with given manifest, as well as in some cases logic for automatically selecting tags based on other user choices or even hardware capabilities.

I created the following Python library that can be used for parsing and evaluating those expressions https://github.com/imLinguin/epic-expreval.

> [!NOTE]
> epic-expreval doesn't implement all functions used in SDLs, as some of them are tied directly to component selection and game/dlc ownership data.  
> For example
> - IsComponentSelected
> - HasAccess