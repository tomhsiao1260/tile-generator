## Introduction

A simple 3D tiles generator. It can generate a set of pseudo `.b3dm` data which can be visualized via [3d-tiles-renderer(https://github.com/NASA-AMMOS/3DTilesRendererJS).

## Setup

Virtual environment
```
python -m venv env
source env/bin/activate
```

Install dependency
```
pip install -r requirements.txt
```

Download [Node.js](https://nodejs.org/en/download/) and install the required npm packages
```bash
cd client && npm install
```

## Run App

Back to the root directory and run this command. It will generate `.b3dm` testing data and corresponding `tileset.json`.
```
cd generate && python app.py
```

Now, we can visualize it on http://localhost:5173/.
```
cd client && npm run dev
```

## Notes

The result looks like [this](https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/327). The generation code is modified from [here](https://github.com/Oslandia/py3dtiles). And follows the `.b3dm` naming convention in [this dataset](https://raw.githubusercontent.com/NASA-AMMOS/3DTilesSampleData/master/msl-dingo-gap/0528_0260184_to_s64o256_colorize/0528_0260184_to_s64o256_colorize/0528_0260184_to_s64o256_colorize_tileset.jso).

