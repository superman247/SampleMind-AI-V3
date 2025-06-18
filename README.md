# SampleMind AI – v3.4

SampleMind AI is a powerful, modular AI-assisted toolkit for managing, organizing, tagging, analyzing, and curating audio samples and loops for FL Studio and all major DAWs.  
**Built for the future:** Python, OpenAI GPT-4o, local fallback AI, blazing-fast CLI, and GUI/plugin-ready architecture.

# 👋 Hi there, I’m @superman247 (Lars Christian Tangen)

I'm a passionate freelancer, AI developer, and creative technologist based in Sandvika, Norway. I specialize in building tools that combine automation, machine learning, and audio processing for musicians, coders, and creators.

---

## 👀 What I’m interested in

- Building intelligent CLI & GUI applications using Python
- Audio analysis, tagging, and organization using AI (librosa, Essentia, TensorFlow, Mistral, GPT)
- Cross-platform development (macOS, Linux, Windows)
- Music production workflows (FL Studio, Vital, sample packs)
- Open source collaboration and tech-for-good innovation
- Web app & plugin design using Electron, Tauri, Flask, FastAPI

---

## 🌱 I’m currently learning

- Advanced Python and AI integration (LLMs, fallback models, audio classification)
- GUI development with Electron, Tailwind, and React
- DevOps & Docker for scalable cross-platform development
- Music DSP theory and plugin architecture

---

## 💞️ I’m looking to collaborate on

- AI-powered audio tools and music plugins
- Open source projects that blend creativity and code
- Early-stage innovation around automation, tagging, and metadata
- Brave browser extensions or micromobility software UX

---

## 📫 How to reach me

- Email: **Lchtangen@gmail.com**
- GitHub: [@superman247](https://github.com/superman247)
- Currently working on: [SampleMind AI](https://github.com/superman247/SampleMind-AI-V3)

---

## 😄 Pronouns
He/Him

---

## ⚡ Fun fact

I use AI to tag, sort, rename, and organize thousands of audio files... for fun 😎🎧

---

<!---
superman247/superman247 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->


---

## 🧠 Core Features

- 🔍 **Auto-tagging:** GPT-4o + local fallback CNN (Hermès)
- 🎛️ **Loop & sample analysis:** BPM, key, genre, mood, instrument
- 🧱 **200+ CLI tools:** Modular, intelligent, extensible
- 📦 **Smart pack builder:** AI-powered curation and export
- 📂 **Folder management:** Automated, tag-driven, and user-friendly
- 🧪 **Full audio toolkit:** librosa, essentia, deep feature extraction
- 🧠 **AI assistant:** GPT-powered, CLI & GUI interface
- 🎚️ **FL Studio/DAW integration:** Ready for plugin and automation
- 🩺 **Metadata management:** Recovery, repair, sync, snapshot, bulk edit
- 🌐 **Plugin system:** Open for community expansion
- 🚀 **Roadmap:** GUI, FL plugin, cross-DAW, and mobile in progress

---

## 📁 Project Structure (v3.4)

- **`cli/options/`** – All CLI modules (sample management, AI tagging, export, processing)
- **`ai_engine/`** – AI models (GPT/Hermès, CNN, ML/feature extraction)
- **`core/`** – Backend and control center, routing, and system logic
- **`data/`** – User sample/loop files, auto/manual tags, project metadata
- **`tests/`** – Automated and integration tests for all core modules
- **`docs/`** – Full documentation and architecture

---

## 🧩 Installation

1. **Clone the repo:**
    git clone [https://github.com/superman247/SampleMindAI.git](https://github.com/larstangen94/SampleMindAI.git)
    cd SampleMindAI

2. **Install Python 3.10+** (use pyenv if needed):
    pyenv install 3.10.10
    pyenv local 3.10.10
    python -m venv .venv
    source .venv/bin/activate

3. **Install dependencies:**
    pip install -r requirements.txt

4. **Run the CLI menu:**
    python -m cli.menu

5. **(Optional) Run all tests:**
    python -m tests.test_all_modules

---

## 🛠️ Development

- Modules live in `cli/options/`
- AI and feature logic: `ai_engine/`
- Core backend: `core/`
- Tests and docs: `tests/`, `docs/`
- Use `config.py` for all paths, batch processing, and logging

---

## 🔄 Contributing

- PRs, new tools, and improvements **welcome!**
- Please add tests for new modules or features.
- Follow our code style (see `CONTRIBUTING.md`).
- Help us shape the next generation of music production software.

---

## 📣 Status

- **CLI Finalization:** All modules now being upgraded for v1.0.0 release.
- **Docs & Index:** Updated with every major commit.
- **Next:** Automated tests, GUI roadmap, plugin/DAW beta.

---

**SampleMind AI (c) 2025 Lars Christian Tangen**  
Open Source. For producers, by producers.
