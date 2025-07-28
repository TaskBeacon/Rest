from psyflow import BlockUnit,StimBank, StimUnit,SubInfo,TaskSettings, TriggerSender
from psyflow import load_config,count_down, initialize_exp
from psychopy import core
import serial
from src import run_trial

# 1. Load config
cfg = load_config()

# 2. Collect subject info
subform = SubInfo(cfg['subform_config'])
subject_data = subform.collect()

# 3. Load task settings
settings = TaskSettings.from_dict(cfg['task_config'])
settings.add_subinfo(subject_data)

# 4. setup triggers
settings.triggers = cfg['trigger_config']
ser = serial.serial_for_url("loop://", baudrate=115200, timeout=1)
# ser = serial.Serial("COM3", baudrate=115200, timeout=1)
if not ser.is_open:
    ser.open()

# Create TriggerSender
trigger_sender = TriggerSender(
    trigger_func=lambda code: ser.write(bytes([1, 225, 1, 0, code])),
    post_delay=0.001
)

# 5. Set up window & input
win, kb = initialize_exp(settings)

# 6. Setup stimulus bank
stim_bank = StimBank(win,cfg['stim_config']).\
            convert_to_voice(['general_instruction', 'EC_instruction', 'EO_instruction', 'good_bye'], voice=settings.voice_name)\
            .preload_all()
# stim_bank.preview_all() 

settings.save_to_json() # save all settings to json file

trigger_sender.send(settings.triggers.get("exp_onset"))
StimUnit('instruction',win,kb)\
    .add_stim(stim_bank.get('general_instruction'))\
    .add_stim(stim_bank.get('general_instruction_voice'))\
    .wait_and_continue()
count_down(win, 3)   
block = BlockUnit(
        block_id=f"block_0",
        block_idx=0,
        settings=settings,
        window=win,
        keyboard=kb
    ).generate_conditions(order='sequential')\
    .on_start(lambda b: trigger_sender.send(settings.triggers.get("block_onset")))\
    .on_end(lambda b: trigger_sender.send(settings.triggers.get("block_end")))\
    .run_trial(func=run_trial, stim_bank=stim_bank, trigger_sender=trigger_sender)
    
    

StimUnit('block',win,kb)\
    .add_stim(stim_bank.get('good_bye'))\
    .add_stim(stim_bank.get('good_bye_voice'))\
    .wait_and_continue(terminate=True)
trigger_sender.send(settings.triggers.get("exp_end"))

ser.close()
core.quit()