# Resting-state Task (EC+EO)

| Field                | Value                        |
|----------------------|------------------------------|
| Name                 |Resting state                 |
| Version              |main |
| URL / Repository     |  https://github.com/TaskBeacon/REST |
| Short Description    | EC + EO                            |
| Created By           | Zhipeng Cao (zhipeng30@foxmail.com)    |
| Date Updated         | 2025/06/21  |
| PsyFlow Version      | 0.1.0      |
| PsychoPy Version     | 2025.1.1    |
| Modality | Behavior/EEG |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |


## 1. Task Overview

This task is a resting‐state paradigm with two conditions—eyes closed (EC) and eyes open (EO)—each presented sequentially in a single block. Participants receive general instructions, complete a brief countdown, then experience alternating EC and EO trials of fixed duration without any active response requirements; triggers mark key events for synchronization.

## 2. Task Flow

### Block-Level Flow

| Step                                 | Description                                                                                                                                                                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Load configuration                   | Call `load_config()` to read `config/config.yaml` and parse subform, task, stimulus, and trigger settings.                                                                                                                                                                                        |
| Collect subject info                 | Instantiate `SubInfo(cfg['subform_config'])` and call `.collect()` to prompt for **subject_id**, **subname**, **age**, and **gender** via a form.                                                                                                                                                  |
| Initialize Task Settings             | Create `TaskSettings.from_dict(cfg['task_config'])`, then `settings.add_subinfo(subject_data)` to store demographics in settings.                                                                                                                                                                  |
| Setup triggers                       | Assign `settings.triggers = cfg['trigger_config']`; open a loopback serial port at 115200 baud; create `TriggerSender` with `trigger_func` writing bytes `[1,225,1,0,code]` and `post_delay=0.001 s`.                                                                                                 |
| Initialize window & input            | Call `initialize_exp(settings)` to open a PsychoPy window with parameters from `window` config and enable keyboard input.                                                                                                                                                                          |
| Setup stimulus bank                  | Instantiate `StimBank(win, cfg['stim_config'])`; call `.convert_to_voice()` on instruction keys (`general_instruction`, `EC_instruction`, `EO_instruction`, `good_bye`); then `.preload_all()`.                                                                                                  |
| Save settings                        | Call `settings.save_to_json()` to export all settings and subject info to a JSON file for record‐keeping.                                                                                                                                                                                         |
| Experiment onset                     | Use `trigger_sender.send(settings.triggers.get("exp_onset"))` to mark the start of the experiment.                                                                                                                                                                                               |
| Present general instructions         | Create `StimUnit('instruction', win, kb)`; add visual and voice versions of `general_instruction`; call `.wait_and_continue()` to display until spacebar press.                                                                                                                                   |
| Countdown                            | Call `count_down(win, 3)` to show a 3-second onscreen countdown.                                                                                                                                                                                                                                 |
| Run block                            | Instantiate `BlockUnit(block_id='block_0', block_idx=0, settings, window=win, keyboard=kb)`; `.generate_conditions(order='sequential')`; `.on_start()` sends `block_onset` trigger; `.on_end()` sends `block_end` trigger; `.run_trial()` loops over conditions using `run_trial` with `stim_bank` and `trigger_sender`. |
| Present goodbye                      | Create `StimUnit('block', win, kb)`; add visual and voice `good_bye` stimuli; call `.wait_and_continue(terminate=True)` to display until final spacebar press and then close.                                                                                                                    |
| Experiment end                       | Use `trigger_sender.send(settings.triggers.get("exp_end"))` to mark the end of the experiment.                                                                                                                                                                                                   |
| Cleanup                              | Close the serial port (`ser.close()`) and call `core.quit()` to exit PsychoPy.                                                                                                                                                                                                                   |

### Trial-Level Flow

| Step                          | Description                                                                                                                                                                                                              |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Initialize trial data         | Create `trial_data = {"condition": condition}` to record the current condition (“EC” or “EO”).                                                                                                                           |
| Create StimUnit factory       | Use `make_unit = partial(StimUnit, win=win, kb=kb, triggersender=trigger_sender)` to simplify subsequent stimulus calls.                                                                                                 |
| Present condition instruction | Call `make_unit(unit_label='inst')`; add `stim_bank.get(f"{condition}_instruction")` and its voice (`..._instruction_voice`); then `.show()` to display until a keypress.                                            |
| Present stimulus              | Call `make_unit(unit_label='stim')`; add `stim_bank.get(f"{condition}_stim")` (EC_stim or EO_stim); then `.show(duration=settings.{condition}_duration, onset_trigger=settings.triggers.get(f"{condition}_onset"), offset_trigger=settings.triggers.get(f"{condition}_offset"))`; finally `.to_dict(trial_data)` to log timestamps. |
| Return trial data             | Return `trial_data`, containing `condition` and any timing/trigger fields added by `.to_dict()`.                                                                                                                         |

## 3. Configuration Summary

### a. Subject Info

| Field       | Meaning                                            |
|-------------|----------------------------------------------------|
| subject_id  | Three-digit integer identifier between 101 and 999 |
| subname     | Subject’s name in Pinyin                           |
| age         | Integer age in years (5–60)                        |
| gender      | Choice: “Male” or “Female”                         |

### b. Window Settings

| Parameter             | Value        |
|-----------------------|--------------|
| size                  | [1920, 1080] |
| units                 | deg          |
| screen                | 1            |
| bg_color              | gray         |
| fullscreen            | True         |
| monitor_width_cm      | 60           |
| monitor_distance_cm   | 72           |

### c. Stimuli

| Name                  | Type     | Description                                                                                                                                                                                                                                               |
|-----------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EO_stim               | text     | A black “+” fixation cross shown at screen center.                                                                                                                                                                                                        |
| EC_stim               | text     | A black text “请闭眼” (“please close your eyes”) shown at screen center.                                                                                                                                                                                  |
| general_instruction   | textbox  | Initial instructions in Chinese (【静息态任务说明】…), displayed centrally (font = SimHei, color = white, letterHeight = 0.78 deg, box size = [20, 5] deg); prompts participants to follow guidance and press space to start.                                      |
| EC_instruction        | textbox  | Eyes-closed instructions in Chinese (“请您闭上眼睛…直到听到提示为止”), centrally displayed with same font, color, size, and units as above.                                                                                                                |
| EO_instruction        | textbox  | Eyes-open instructions in Chinese (“请您睁开眼睛…直到听到提示为止”), centrally displayed with same properties.                                                                                                                                                |
| good_bye              | textbox  | End-of-task screen in Chinese (“任务结束\n\n感谢您的参与\n请按【空格键】键退出”), centrally displayed with same font, color, letterHeight, and box size.                                                                                                  |

### d. Timing

| Phase   | Duration    |
|---------|-------------|
| EC      | 180 seconds |
| EO      | 180 seconds |

### e. Triggers

| Event        | Code |
|--------------|------|
| exp_onset    | 98   |
| exp_end      | 99   |
| block_onset  | 100  |
| block_end    | 101  |
| EC_onset     | 10   |
| EC_offset    | 11   |
| EO_onset     | 20   |
| EO_offset    | 21   |

## 4. Methods
The experiment consists of one block containing four sequential rest trials: eyes closed (EC), eyes open (EO), eyes closed (EC), and eyes open (EO), each lasting 180 s for a total data collection time of 720 s (12 minutes).Participants first provide demographic information (ID, name in Pinyin, age, gender) via a modal form. After settings and triggers initialize, they view general task instructions in Chinese, followed by a 3‑second on‑screen countdown. Each trial begins with an on‑screen text instruction and its pre‑recorded voice version. Immediately afterward, the resting‑state stimulus (a central fixation cross for EO trials or the text “请闭眼” ("close your eyes") for EC trials) appears for exactly 180 s. The display window is set to 1920×1080 pixels in degrees of visual angle, with a gray background and a viewing distance of 72 cm. 
