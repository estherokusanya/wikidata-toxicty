# Evaluating Toxicity in Knowledge Graphs and it's Effects in Downstream Tasks

Code Base Accompanying Paper: [link to my paper]

## Description

This repo accompanies research on bias in collaborative KGs (Wikidata). We propose a novel approach to identify toxicity bias by transforming KG entities & relationships into natural language utilising teh verbaliser present in WDV. This allows us to leverage established metrics for evaluating large language models (LLMs) to assess KG bias. The KGQA and the Link Prediction system are also present  also investigate how KG toxicity affects downstream AI systems like LLMs and recommendation systems.


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* pip
  ```sh
  python3 -m pip install --upgrade pip
  ```

### Installation

1. Set up accounts and get a free API Key from: (billing details required)
    OpenAI: https://platform.openai.com/
    Llama: https://www.llama-api.com/
    Mistral Ai: https://mistral.ai/
    Ai21: https://www.ai21.com/studio

2. Clone the repo with its submodules
   ```sh
   git clone --recurse-submodules https://github.com/estherokusanya/Project-Name.git
   ```
3. Follow steps in [WDV](https://github.com/gabrielmaia7/WDV/tree/13810bd80e2c64956018b5ae508f6eb582deaf3c/Verbalisation) to unpack *graph2text*
4. Update package location in `verbalisation_module.py`
    ```python
        DATA_DIR = 'helpers/WDV/verbalisation/graph2text/data/webnlg'
        OUTPUT_DIR = 'helpers/WDV/verbalisation/graph2text/outputs/test_model'
        CHECKPOINT = 'helpers/WDV/verbalisation/graph2text/outputs/t5-base_13881/val_avg_bleu=68.1000-step_count=5.ckpt'
    ```
3. (Optional) Create a virtual environment
   ```sh
   python3 -m venv <name_of_virtualenv>
   ```
4. Install dependencies from .requirements file
    ```sh
   pip install -r requirements.txt
   ```
5. Enter your API in `.env`
   ```js
    OPENAI_KEY = 'ENTER YOUR API KEY'
    LLAMA_KEY= ''
    JURASSIC_KEY = ''
    MISTRAL_KEY= ''
    PERSPECTIVEAPI_KEY= ''
   ```



<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

ex. Esther Okusanya
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

* [readme template](https://github.com/matiassingers/awesome-readme)
* [WDV](https://github.com/gabrielmaia7/WDV)
