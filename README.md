[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/FF1Kikho)

# Generative AI and Large Language Model

### Team Members:
- Srishti Chouhan (schouhan)
- Bhaavanaa Thumu (bthumu)

### Topic: Use Case #2 - Provide up-to-date weather information (and forecasts)

### Video URL: [Link to Video]

## Files:

### `application.py`: 
This file contains the code for the Streamlit web application that utilizes the OpenWeatherMap API and Vertex AI models (gemini-pro and text-bison) to display current weather information and forecasts for a selected city. It also uses LangChain to generate descriptive responses based on templates for weather-related prompts.

### `models_eval.ipynb`: 
This Jupyter Notebook contains the code for comparing the two language models (text-bison and gemini-pro) using gpt-4 through prompts. It scores their responses and generates a radar plot comparing their performance across various dimensions, providing a fine-grained assessment.

---

## Required Libraries:

Create a conda environment with the following libraries:

```bash
conda create --name your_env_name python=3.9.18
conda activate your_env_name
conda install -c conda-forge streamlit=1.31.1
conda install -c conda-forge google-cloud-aiplatform=1.43.0
conda install -c conda-forge langchain-google-vertexai=0.1.0
conda install -c conda-forge langchain=0.1.9
