from ippa.episode import Episode


def read_processes(patient, procs, read_end):
    recs = patient.Records
    for sub in procs.values():
        sub.start()

    recs_collected = list()
    for rec in recs:
        collected = False
        for sub in procs.values():
            collected |= sub.update(rec.Events, rec.Time)
        if collected:
            recs_collected.append(rec)

    # todo timing
    dea = patient.LeavingDay
    if recs[-1].Time <= dea < read_end:
        for sub in procs.values():
            sub.die(dea)
    else:
        for sub in procs.values():
            sub.end(read_end)

    # combine results
    history, cuts = list(), list()
    times = set()
    for v in procs.values():
        times.update([st.Time for st in v.History])
    times = list(times)
    times.sort(reverse=False)

    for ti in times:
        cut = True
        sts = {'Time': ti}
        for k, v in procs.items():
            st = v.at(ti)
            sts[k] = st
            cut &= st is v.DefaultState

        if cut:
            cuts.append(ti)
        history.append(sts)
    return recs_collected, cuts, history


def cut_episodes(patient, collected, cuts, history):
    recs = list(collected)
    es = list()
    hs = list()

    for fr, to in zip(history[:-1], history[1:]):
        hs.append(to)
        ti = to['Time']
        if ti in cuts:
            rs = [rec for rec in recs if rec.Time < ti]
            recs = [rec for rec in recs if rec.Time >= ti]
            es.append(Episode(patient.ID, hs, rs))
            hs = list()
    es.append(Episode(patient.ID, hs, recs))
    return es

