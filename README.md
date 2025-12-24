# AIMO Progress Prize 3 - Ensemble Solution

Competition solution for AI Mathematical Olympiad Progress Prize 3 using ensemble of math-specialized LLMs with Tool-Integrated Reasoning (TIR) and smart voting.

**Competition**: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3
**Live Notebook**: https://www.kaggle.com/code/piyushksinghh/aimo-p3-ensemble-all-strategies

---

## 📁 Project Structure

```
AIMO-P3/
├── kaggle_data/              # Data from Kaggle
│   └── competition_data/
│       ├── reference.csv     # 10 IMO test problems
│       ├── test.csv          # Competition test format
│       └── sample_submission.csv
│
├── notebooks/                # Kaggle notebooks (ready to push)
│   ├── ensemble/
│   │   ├── ensemble_all_strategies.ipynb  # Main solution notebook
│   │   └── kernel-metadata.json           # Kaggle configuration
│   └── submission/
│       ├── qwen_1.5b_multi_strategy.ipynb  # Single model, 5 strategies (reference)
│       └── kernel-metadata.json            # Kaggle configuration
│
├── scripts/                  # Supporting scripts
│   ├── push_notebook.py          # Push notebook to Kaggle
│   └── get_notebook_logs.py      # Fetch Kaggle execution logs
│
├── logs/                     # Downloaded execution logs
├── shell.nix                 # Nix environment
└── README.md                 # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
nix-shell  # Activates Python, Kaggle API, and dependencies
```

### 2. Develop Locally
```bash
# Edit the main notebook
notebooks/ensemble/ensemble_all_strategies.ipynb

# Set TEST_MODE = True in cell-0 for local testing
```

### 3. Deploy to Kaggle
```bash
# Push ensemble notebook (default)
python3 scripts/push_notebook.py

# Or push submission notebook
python3 scripts/push_notebook.py submission
```

### 4. Monitor Execution
```bash
# Get logs for ensemble notebook (default)
python3 scripts/get_notebook_logs.py

# Or get logs for submission notebook
python3 scripts/get_notebook_logs.py submission
```

### 5. Submit to Competition
1. Wait for notebook to complete without errors
2. Set `TEST_MODE = False` in cell-0
3. Run `python3 scripts/push_notebook.py` again
4. In Kaggle UI, click "Submit to Competition"

---

## 🧠 Solution Architecture

### Models (4 Different LLMs)
1. **Qwen2.5-Math-1.5B** - Fast baseline (3 samples)
2. **Qwen2.5-Math-7B** - Main workhorse (6 samples, 3 temperatures)
3. **DeepSeek-Math-7B-RL** - RL-trained specialist (6 samples, 3 temperatures)
4. **MAmmoTH-7B-Mistral** - Math-supervised (3 samples)

**Total**: 18-20 samples per problem

### Key Techniques
- ✅ **Tool-Integrated Reasoning (TIR)**: Models can write and execute Python code
- ✅ **Self-Consistency**: Multiple samples per model with voting
- ✅ **Smart Voting**: Filters outliers, requires >40% consensus
- ✅ **Sequential Loading**: Avoids GPU OOM by loading one model at a time

### Based on AIMO Prize Winners
- **Prize 1 (Numina)**: 29/50 problems - Used TIR with 48 samples
- **Prize 2 (NemoSkills)**: 34/50 problems - TIR + generative selection

---

## 📊 Current Status

### ✅ What Works
- Runs without errors on Kaggle
- Creates valid `submission.parquet`
- All 4 models load and generate predictions
- Smart voting implemented

### ⚠️ What Needs Improvement
- **Low accuracy** (~0-1/10 on reference problems)
- Models struggle with IMO-level complexity
- TIR not being used effectively (models rarely generate code)

### 🎯 Next Steps
1. **Better Prompts**: Add few-shot examples with solved IMO problems
2. **More Samples**: Increase from 20 to 48+ like winners
3. **Better Models**: Search for IMO/AIME fine-tuned models
4. **Analysis**: Debug why models produce wrong answers

---

## 📝 Key Files

### Main Notebook
**[notebooks/ensemble/ensemble_all_strategies.ipynb](notebooks/ensemble/ensemble_all_strategies.ipynb)**
- Source of truth for all development
- Has `TEST_MODE` flag:
  - `True`: Runs on reference.csv for testing
  - `False`: Serves gRPC for competition submission

### Configuration
**[notebooks/ensemble/kernel-metadata.json](notebooks/ensemble/kernel-metadata.json)**
```json
{
  "id": "piyushksinghh/aimo-p3-ensemble-all-strategies",
  "dataset_sources": [
    "kaizinzheng/qwen2-5-math-1-5b-instruct",
    "gmhost/qwen2-5-math-7b-instruct",
    "christianmariothomas/deepseek-math-7b-rl",
    "elvenmonk/mammoth-7b-mistral"
  ],
  "competition_sources": ["ai-mathematical-olympiad-progress-prize-3"]
}
```

### Scripts
- **[scripts/push_notebook.py](scripts/push_notebook.py)**: Push notebook to Kaggle
  ```bash
  python3 scripts/push_notebook.py [notebook_name]
  # notebook_name: ensemble (default) or submission
  ```
- **[scripts/get_notebook_logs.py](scripts/get_notebook_logs.py)**: Download logs and output files
  ```bash
  python3 scripts/get_notebook_logs.py [notebook_name]
  # notebook_name: ensemble (default) or submission
  # Logs saved to: ./logs/{notebook_name}/
  ```

---

## 🔧 Development Workflow

### Testing Changes
```bash
# 1. Edit notebooks/ensemble/ensemble_all_strategies.ipynb
# 2. Ensure TEST_MODE = True
# 3. Push to Kaggle
python3 scripts/push_notebook.py ensemble

# 4. Wait ~3-4 hours for completion
# 5. Check results
python3 scripts/get_notebook_logs.py ensemble
```

### Making a Submission
```bash
# 1. Set TEST_MODE = False in cell-0
# 2. Push to Kaggle
python3 scripts/push_notebook.py

# 3. In Kaggle UI:
#    - Go to your notebook
#    - Click "Submit to Competition"
#    - Wait for evaluation
```

---

## 📚 References

### Competition
- [AIMO Progress Prize 3](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3)
- [AIMO Prize Official Site](https://aimoprize.com/)

### Winning Solutions
- [Numina (Prize 1 Winner)](https://huggingface.co/blog/winning-aimo-progress-prize)
- [NemoSkills (Prize 2 Winner)](https://arxiv.org/pdf/2504.16891)

### Our Notebook
- [Live Kaggle Notebook](https://www.kaggle.com/code/piyushksinghh/aimo-p3-ensemble-all-strategies)

---

## 🐛 Troubleshooting

### "Maximum batch GPU session count reached"
- Kaggle allows max 2 concurrent GPU sessions
- Wait for previous runs to complete or cancel them

### "submission.parquet not found"
- Ensure notebook creates the file
- Set `TEST_MODE = False` for actual submission
- Check logs with `get_notebook_logs.py`

### "Protobuf error"
- Fixed in v11+ by only creating inference_server in submission mode
- Don't create server object when TEST_MODE = True

---

## 📈 Version History

- **v11** (Current): Smart voting + TIR, protobuf fix
- **v10**: All 4 models, 20 samples, TIR enabled
- **v7**: First working 4-model ensemble
- **v1-6**: Initial development and testing

---

## 🤝 Contributing

This is a competition entry, but feel free to:
- Review the approach
- Suggest improvements
- Learn from the techniques used

**Good luck solving IMO problems with AI!** 🎓
