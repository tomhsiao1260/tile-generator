## Introduction

A simple 3D tiles generator. It can generate a set of pseudo `.b3dm` data which can be visualized via [3d-tiles-renderer](https://github.com/NASA-AMMOS/3DTilesRendererJS).

## Setup

Virtual environment

```bash
python -m venv env
source env/bin/activate
```

Install dependency

```bash
pip install -r requirements.txt
```

Download [Node.js](https://nodejs.org/en/download/) and install the required npm packages

```bash
cd client && npm install
```

## Run App

Back to the root directory and run this command. It will generate `.b3dm` testing data and corresponding `tileset.json`.

```bash
cd generate && python app.py
```

Back to the root directory again. Now, we can visualize it on http://localhost:5173/

```bash
cd client && npm run dev
```

In `app.py`, `depth` means how many `.b3dm` cubes that you want to generate.
```
// cube numbers
depth 0:  1
depth 1:  1 + 2^3
depth 2:  1 + 2^3 + 4^3
...
```

## Notes

The result looks like [this](https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/327). The generation code is modified from [here](https://github.com/Oslandia/py3dtiles). And follows the `.b3dm` naming convention in [this dataset](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/example/mars.js#L70).

