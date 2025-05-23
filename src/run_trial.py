from psyflow import StimUnit
from functools import partial

def run_trial(win, kb, settings, condition, stim_bank, trigger_sender):

    trial_data = {"condition": condition}

    make_unit = partial(StimUnit, win=win, kb=kb, triggersender=trigger_sender)
    
    # --- instruction ---
    make_unit(unit_label='inst').add_stim(stim_bank.get(f"{condition}_instruction")) \
    .add_stim(stim_bank.get(f"{condition}_instruction_voice")) \
    .show()

    # --- stim ---
    make_unit(unit_label='stim').add_stim(stim_bank.get(f"{condition}_stim")) \
        .show(duration=getattr(settings, f"{condition}_duration"), 
              onset_trigger=settings.triggers.get(f"{condition}_onset"), 
              offset_trigger=settings.triggers.get(f"{condition}_offset")) \
        .to_dict(trial_data)

    return trial_data
