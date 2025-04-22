from psyflow import TrialUnit
from functools import partial

def run_trial(win, kb, settings, condition, stim_bank, trigger_sender, trigger_bank):
    """
    Run a single MID trial sequence (fixation → cue → anticipation → target → feedback).
    See full docstring above...
    """

    trial_data = {"condition": condition}

    make_unit = partial(TrialUnit, win=win, triggersender=trigger_sender)
    
    # --- instruction ---
    make_unit(unit_label='inst').add_stim(stim_bank.get(f"{condition}_instruction")) \
    .wait_and_continue().to_dict(trial_data)  

    # --- stim ---
    make_unit(unit_label='stim').add_stim(stim_bank.get(f"{condition}_stim")) \
        .show(duration=getattr(settings, f"{condition}_duration"), onset_trigger=trigger_bank.get(f"{condition}_onset")) \
        .to_dict(trial_data)

    return trial_data
