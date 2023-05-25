import os
import openai
openai.api_key = "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"


def predictSalary(jobname):
    c =  openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {f"role": "user", "content": 'Donner moi une approximation  d\' intervalle de salaire de '+jobname+' en tunisie par mois, nombres seulement en reponse'}
        ]
    )

    Respone  = c["choices"][0]["message"]["content"]

    Response = Respone.split()
    salaries = []

    for r in Response:
        try:
            s = float(r)
            salaries.append(s)
        except:
            continue
    
    return salaries