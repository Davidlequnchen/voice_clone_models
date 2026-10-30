# voice_clone_models

Model files for the voice-cloning part of
[Davidlequnchen/emotion_recognition](https://github.com/Davidlequnchen/emotion_recognition) (`antideepfake/`), for a
computer that cannot reach Hugging Face or ModelScope. Files over 90 MiB are stored as 90 MiB parts with a SHA-256;
`join_parts.py` puts them back together. The files are unmodified copies from the sources below, at the pinned
revisions of `antideepfake/config/voice_clone.yaml`; only the files the inference code reads are included.

## Use

```bash
cd emotion_recognition/antideepfake/models
git clone https://github.com/Davidlequnchen/voice_clone_models.git voice_clone   # this folder: models/voice_clone/
cd voice_clone && python join_parts.py        # joins the parts and checks every SHA-256
cd ../.. && python scripts/voice_clone/download_models.py   # clones the CosyVoice code from GitHub; skips the models
python scripts/voice_clone/generate.py
```

## Contents

| Folder | Model | Source (revision) | Licence | Size |
|---|---|---|---|---|
| `cosyvoice2_0.5b/` | CosyVoice2-0.5B | [HF FunAudioLLM/CosyVoice2-0.5B](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B) (`eec1ae6c79877dbd9379285cf8789c9e0879293d`) | Apache-2.0 | 3.09 GB |
| `cosyvoice3_0.5b/` | Fun-CosyVoice3-0.5B-2512 | [HF FunAudioLLM/Fun-CosyVoice3-0.5B-2512](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) (`29e01c4e8d000f4bcd70751be16fa94bf3d85a18`) | Apache-2.0 | 4.44 GB |
| `chatterbox/` | Chatterbox (English) | [HF ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) (`5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18`) | MIT | 3.19 GB |
| `wetext/` | wetext text-normalisation FSTs (en, zh) | [ModelScope pengzhendong/wetext](https://www.modelscope.cn/models/pengzhendong/wetext) (`67928a15fac1e769e23189c53648a65dea206a39`) | Apache-2.0 | 11 MB |

Each folder keeps its model card (`README.md`) from the source. Papers: CosyVoice 2,
[arXiv:2412.10117](https://arxiv.org/abs/2412.10117); CosyVoice 3, [arXiv:2505.17589](https://arxiv.org/abs/2505.17589);
Chatterbox has no paper ([GitHub resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)).

## Updating the weights

After downloading new files into these folders: `python split_parts.py` (FILES at its top lists the large files),
then commit the parts and `.sha256` files in batches of at most 15 parts per push (GitHub refuses pushes over 2 GB
and files over 100 MB).
