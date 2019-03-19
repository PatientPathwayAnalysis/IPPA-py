from collections import OrderedDict
from tb.stages import TBStage


def is_eligible_episode(episode):
    ser = episode.History
    if [s for s in ser if s['Tre'] in ['1st', '2nd']]:
        return True
    else:
        return False


def identify_critical_stages(episode, read_end):
    ser = episode.History
    anchors = OrderedDict()
    entry = ser[0]
    anchors['StartTime'] = entry['Time']
    anchors['EndTime'] = ser[-1]['Time']

    if entry['Tre'] == '1st':
        anchors['StartEvent'] = TBStage.TREATING_F
    elif entry['Tre'] == '2st':
        anchors['StartEvent'] = TBStage.TREATING_S
    elif entry['Tre'] == 'Empirical':
        anchors['StartEvent'] = TBStage.EVALUATING_H
    elif entry['Eva'] == 'Strong':
        anchors['StartEvent'] = TBStage.EVALUATING_H
    elif entry['Eva'] == 'Weak':
        anchors['StartEvent'] = TBStage.EVALUATING_L
    else:
        anchors['StartEvent'] = TBStage.WAITING

    # Confirmation
    for entry in ser:
        if entry['Tre'] in ['1st', '2nd']:
            anchors['ConfirmationTime'] = entry['Time']
            break

    # Evaluation
    if anchors['StartEvent'] is not TBStage.WAITING:
        anchors['EvaluatingTime'] = anchors['StartTime']
    else:
        for entry in ser:
            if entry['Time'] >= anchors['ConfirmationTime']:
                anchors['EvaluatingTime'] = anchors['ConfirmationTime']
                break
            elif any([entry['Tre'] != 'None', entry['Eva'] != 'None']):
                anchors['EvaluatingTime'] = entry['Time']
                break

    for entry in ser:
        if entry['Time'] >= anchors['ConfirmationTime']:
            anchors['DetectingTime'] = anchors['ConfirmationTime']
            break
        elif any([entry['Tre'] == 'Empirical', entry['Eva'] == 'Strong']):
            anchors['DetectingTime'] = entry['Time']
            break

    if anchors['ConfirmationTime'] > anchors['EvaluatingTime']:
        anchors['Evaluations'] = [s for s in ser
                                  if anchors['EvaluatingTime'] <= s['Time'] < anchors['ConfirmationTime']]
    else:
        anchors['Evaluations'] = list()

    # Treatment
    tic = anchors['ConfirmationTime']
    tit = anchors['StartTime']
    if tic > anchors['StartTime']:
        ser_t = [s for s in ser if s['Time'] <= tic]
        for entF, entT in zip(ser_t[:1], ser_t[1:]):
            if entF['Tre'] == 'None' and entT['Tre'] != 'None':
                tit = entT['Time']
        anchors['TreatmentTime'] = tit
    else:
        anchors['TreatmentTime'] = anchors['StartTime']

    ser_e = [s for s in ser if s['Time'] > tic]
    ser_e.reverse()
    ti = read_end
    for ent in ser_e:
        if ent['Tre'] not in ['None', 'Dead']:
            break
        ti = ent['Time']
    anchors['TreatmentEnd'] = ti

    anchors['Treatments'] = [s for s in ser if anchors['ConfirmationTime'] <= s['Time'] < anchors['TreatmentEnd']]
    anchors['TreatmentPeriod'] = anchors['TreatmentEnd'] - anchors['TreatmentTime']

    # post = set([h['Eva'] for h in episode.History if h['Time'] >= anchors['TreatmentEnd']])

    if ser[-1]['Tre'] == 'Dead':
        anchors['Outcome'] = TBStage.DEAD
    elif anchors['TreatmentPeriod'] > 7*4*6:
        anchors['Outcome'] = TBStage.COMPLETED
    elif ser[-1]['Time'] >= read_end:
        anchors['Outcome'] = TBStage.CENSORED
    # elif len(post) > 1:
    #    anchors['Outcome'] = TBStage.EARLY
    else:
        anchors['Outcome'] = TBStage.LOST

    return anchors


def form_pathway(episode):
    pat = list()
    anchors = episode.Anchors
    stage = anchors['StartEvent']
    pat.append({'Time': anchors['StartTime'], 'Stage': anchors['StartEvent']})

    los_e, los_d = False, False
    for eva in anchors['Evaluations']:
        if stage is TBStage.WAITING:
            if eva['Eva'] == 'Weak':
                stage = TBStage.EVALUATING_L
                pat.append({'Time': eva['Time'], 'Stage': stage})
            elif eva['Eva'] == 'Strong' or eva['Tre'] == 'Empirical':
                stage = TBStage.EVALUATING_H
                pat.append({'Time': eva['Time'], 'Stage': stage})

        elif stage is TBStage.EVALUATING_L:
            if eva['Eva'] == 'Strong' or eva['Tre'] == 'Empirical':
                stage = TBStage.EVALUATING_H
                pat.append({'Time': eva['Time'], 'Stage': stage})
            elif all([eva['Eva'] == 'None', eva['Tre'] == 'None', eva['Pre'] != 'None']):
                stage = TBStage.IE
                pat.append({'Time': eva['Time'], 'Stage': stage})

        elif stage is TBStage.EVALUATING_H:
            if all([eva['Eva'] == 'None', eva['Tre'] == 'None', eva['Pre'] != 'None']):
                stage = TBStage.IE
                pat.append({'Time': eva['Time'], 'Stage': stage})

        elif stage is TBStage.IE:
            if eva['Eva'] == 'Weak':
                stage = TBStage.REEVALUATING_L
                pat.append({'Time': eva['Time'], 'Stage': stage})
            elif eva['Eva'] == 'Strong' or eva['Tre'] == 'Empirical':
                stage = TBStage.REEVALUATING_H if los_d else TBStage.EVALUATING_H
                pat.append({'Time': eva['Time'], 'Stage': stage})

        elif stage is TBStage.REEVALUATING_L:
            if eva['Eva'] == 'Strong' or eva['Tre'] == 'Empirical':
                stage = TBStage.REEVALUATING_H if los_d else TBStage.EVALUATING_H
                pat.append({'Time': eva['Time'], 'Stage': stage})
            elif all([eva['Eva'] == 'None', eva['Tre'] == 'None', eva['Pre'] != 'None']):
                stage = TBStage.IE
                pat.append({'Time': eva['Time'], 'Stage': stage})

        elif stage is TBStage.REEVALUATING_H:
            if all([eva['Eva'] == 'None', eva['Tre'] == 'None', eva['Pre'] != 'None']):
                stage = TBStage.IE
                pat.append({'Time': eva['Time'], 'Stage': stage})

    tre = anchors['Treatments'][0]
    stage = TBStage.TREATING_F if tre['Tre'] == '1st' else TBStage.TREATING_S
    if stage is not pat[-1]['Stage']:
        pat.append({'Time': tre['Time'], 'Stage': stage})

    first = True

    for tre in anchors['Treatments'][1:]:
        if first:
            if tre['Tre'] != '1st':
                stage = TBStage.TC
                pat.append({'Time': tre['Time'], 'Stage': stage})
                if tre['Tre'] == '2nd':
                    stage = TBStage.TREATING_S
                    pat.append({'Time': tre['Time'], 'Stage': stage})
                first = False

        else:
            if tre['Tre'] != 'None':
                if stage is not TBStage.TREATING_S:
                    stage = TBStage.TREATING_S
                    pat.append({'Time': tre['Time'], 'Stage': stage})
            elif stage is not TBStage.TC:
                stage = TBStage.TC
                pat.append({'Time': tre['Time'], 'Stage': stage})

    if stage is TBStage.TC:
        pat.pop()
    pat.append({'Time': anchors['TreatmentEnd'], 'Stage': anchors['Outcome']})
    return pat


def is_eligible_pathway(episode):
    return episode.Attributes['TreatmentPeriod'] >= 28
