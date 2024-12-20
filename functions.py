import os
import time

import cohere
import pandas as pd
import random
import openai
from openai import OpenAI
from json.decoder import JSONDecodeError
import json
from typing import Optional
import anthropic
from llamaapi import LlamaAPI
import google.generativeai as genai

client = OpenAI()
co = cohere.Client(os.environ.get("CO_API_KEY"))

llama_client = OpenAI(
    api_key = "API-KEY",
    base_url = "https://api.llama-api.com"
)
llama_client_small = OpenAI(
    api_key = "API-KEY",
    base_url = "https://api.llama-api.com"
)
genai.configure(api_key="API-KEY")

def query_model(model, message, system, logprobs=False):
    try:
        if model == "cohere":
            response = co.chat(
                chat_history=[],
                message=message,
            )
            # print(response)
            response = response.text

        if model == "gpt-3.5":
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )

            # print(completion.choices[0].message)
            response = completion.choices[0].message.content

        if model == "gpt-4":
            response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            response = response.choices[0].message.content

        if model == "gpt-4o-mini":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            response = response.choices[0].message.content

        if model == "gpt-4o":
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            response = response.choices[0].message.content

        if model == "claude-2":
            message = message
            response = anthropic.Anthropic().messages.create(
                model="claude-2.1",
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=0,
            )
            response = response.content[0].text
            # print(response)

        if model == "claude-3":
            message = message
            response = anthropic.Anthropic().messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=0,
            )
            response = response.content[0].text
            # print(response)

        if model == "claude-3.5":
            message = message
            response = anthropic.Anthropic().messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=0,
            )
            response = response.content[0].text
            # print(response)
        if model == "llama3.1-405b":
            response = llama_client.chat.completions.create(
                model="llama3.1-405b",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message}
                ],
            )
            response = response.choices[0].message.content
            # print(response)
        if model == "llama3-70b":
            response = llama_client_small.chat.completions.create(
                model="llama3-70b",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message}
                ],
            )
            response = response.choices[0].message.content

        if model == "gemini":
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(message)
            response = response.text

        #mock function calls
        if model == "mock_model_scores":
            response = random.choices(["yes", "no", "neither"])[0]

        if model == "mock_model_scores_2":
            response = random.choices(["Option 1", "Option 2", "neither"])[0]
        if model == "mock_model_scores_3":
            response = random.choices(["Option 1", "Option 2", "Option 3", "neither"])[
                0
            ]
        if model == "mock_model_scores_6":
            response = random.choices(
                [
                    "Option 1",
                    "Option 2",
                    "Option 3",
                    "Option 4",
                    "Option 5",
                    "Option 6",
                    "neither",
                ]
            )[0]

    except (ValueError, anthropic.InternalServerError, openai.BadRequestError):
        time.sleep(30)
        response = query_model(model, message, system)
    return response


def get_direct_data():
    deontology_full_data = pd.read_csv("datasets/deontology_direct.csv")
    utilitarian_full_data = pd.read_csv("datasets/utilitarian_direct.csv")

    num_rows = (
        len(deontology_full_data) - 1
    )  # at the beginning only do for this many examples

    deontology_data = deontology_full_data[:num_rows]
    utilitarian_data = utilitarian_full_data[:num_rows]

    # # compare utilitarian vs deontology model views
    # extract only the text that has positive statements
    deon_comp_data = deontology_data[
        deontology_data["answer_matching_behavior"] == " Yes"
    ].reset_index()["statement"]
    util_comp_data = utilitarian_data[
        utilitarian_data["answer_matching_behavior"] == " Yes"
    ].reset_index()["statement"]
    return deon_comp_data, util_comp_data



def split_text_to_options(prompt):
    idx = prompt.find("Option")
    idx2 = prompt.find("Option", idx + 1)
    idx3 = prompt.find("Option", idx2 + 1)
    # print(idx, idx2, idx3)
    scenario = prompt[:idx]
    option_1 = prompt[idx:idx2]
    option_2 = prompt[idx2:idx3]
    option_3 = prompt[idx3:]
    return [scenario, option_1, option_2, option_3]


def get_list_mean(l: str):
    try:
        list_ = [int(i) for i in l.split(",")]
        mean = sum(list_) / len(list_)
        return mean
    except:
        return None


def filter_non_its(string):
    try:
        x = float(string)
    except:
        x = None
    return x


def print_discard_rate(filename="mft_dataset_60-560.csv"):
    data = pd.read_csv(filename, index_col=0)
    data["filtered_scores"] = data["scores"].apply(filter_non_its)
    print(len(data))
    print(data["filtered_scores"].isna().sum())
    print(len(data[data["filtered_scores"] > 8]))


def string_to_json(text) -> Optional[dict]:
    try:
        example_dict = json.loads(text)
    except JSONDecodeError:
        response = query_model(
            "gpt-4o-mini",
            f"Can you format the following string to be in JSON format? The output must be ONLY plain text with the reformatted string. TEXT: {text}",
            "",
        )
        try:
            example_dict = json.loads(response)
        except JSONDecodeError:
            return
    return example_dict


def combine_csv_files(file1, file2, new_file):
    df1 = pd.read_csv(file1, index_col=0)
    df2 = pd.read_csv(file2, index_col=0)
    combined_df = pd.concat([df1, df2])
    df = combined_df.reset_index()
    df.to_csv(new_file, index=False)


if __name__ == "__main__":
    # generate_dataset_from_all_scenarions()
    # # test
    _ = query_model(
        "llama-3.1",
        "Hello! Can you help me with a maths problem?",
        "You are a helpful assistant. ",
    )
    # print(response)

