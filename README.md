# Resting-State Task – PsyFlow Version

This task presents two resting-state conditions — **Eyes Open (EO)** and **Eyes Closed (EC)** — while recording neural signals (e.g., EEG, fMRI). It is implemented using the [PsyFlow](https://taskbeacon.github.io/psyflow/) framework.



## Task Overview

Participants are instructed to either fixate on a cross (Eyes Open) or close their eyes and relax (Eyes Closed). Each condition lasts for a fixed duration of 5 minutes (300 seconds). There is no need to respond during the task. Instructions are shown before each condition and a goodbye screen concludes the session.

This task is suitable for studies on baseline brain activity, spontaneous fluctuations, default mode network (DMN) activity, or physiological noise calibration.



## Task Flow

| Step        | Description |
|-|-|
| General Instruction | A textbox introduces the resting-state paradigm. Participant presses **space bar** to continue. |
| Condition Instruction | A textbox explains the upcoming condition (EO or EC). Press **space bar** to proceed. |
| Stimulation | The fixation cross or blank screen is presented for **300 seconds**, depending on the condition. |
| Goodbye     | A textbox thanks the participant and prompts exit with **space bar**. |



## Configuration Summary

All key settings are stored in the `config.yaml` file. Here's a breakdown of relevant sections:

### Subject Info (`subinfo_fields`)
Participants are registered with:
- **Subject ID** (3-digit number from 101–999)
- **Session name** (e.g., Practice, Experiment)
- **Experimenter name**
- **Gender** (Male or Female)

These fields are localized to Chinese via `subinfo_mapping`.



### Window Settings (`window`)
- Resolution: `1920 × 1080`
- Units: `deg`
- Fullscreen: `True`
- Monitor: `testMonitor`
- Background color: `black`



### Stimuli (`stimuli`)
| Stimulus       | Type     | Notes |
|-|-|-|
| `general_instruction` | `textbox` | General task instruction in Chinese |
| `EO_instruction`      | `textbox` | Instruction for eyes-open condition |
| `EC_instruction`      | `textbox` | Instruction for eyes-closed condition |
| `EO_stim`             | `text`    | Fixation cross `"+"` |
| `EC_stim`             | `text`    | Blank screen |
| `good_bye`            | `textbox` | Final thank-you screen |

All textboxes use `SimHei` font, are center-aligned, and designed for full-screen presentation.



### Timing (`timing`)
- `EO_duration`: `300` seconds
- `EC_duration`: `300` seconds

Each condition runs for 5 minutes, customizable in the config.



### Triggers (`triggers`)
The following triggers are sent via `TriggerSender`:

- **Experiment**: `exp_onset = 98`, `exp_end = 99`
- **Block**: `block_onset = 100`, `block_end = 101`
- **Eyes Closed**: `EC_onset = 10`, `EC_offset = 11`
- **Eyes Open**: `EO_onset = 20`, `EO_offset = 21`

These are intended for synchronizing external hardware (e.g., EEG or eye tracker).



## Running the Task

1. Make sure all dependencies are installed (see below).
2. Launch the experiment via:

```bash
python main.py
```
