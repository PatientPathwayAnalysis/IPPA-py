import datetime
from collections import OrderedDict
from tb.stages import TBStage


def count_event(rec, hos):
    try:
        tb = rec.Events['Main']
        if tb.Drugs:
            hos.count('Anti-TB')

        proc = tb.Procedures
        if proc:
            if proc.Types['H']:
                hos.count('EH-TB')
            if proc.Types['L']:
                hos.count('EL-TB')
    except KeyError:
        return


def summary(episode):
    statistics = OrderedDict()
    day0 = datetime.datetime(2001, 1, 1)
    anc = episode.Anchors

    stage_starts = OrderedDict()
    stage_starts['Waiting'] = anc['StartTime']
    stage_starts['Evaluating'] = anc['EvaluatingTime']
    stage_starts['Detecting'] = anc['DetectingTime']
    stage_starts['Treating'] = anc['ConfirmationTime']
    stage_starts['TreatmentEnd'] = anc['TreatmentEnd']

    statistics['HospitalStart'] = episode.Records[0].Hospital
    statistics['StageStart'] = anc['StartEvent'].name
    statistics['YearStart'] = (datetime.timedelta(days=stage_starts['Waiting']) + day0).year
    # statistics['Cross2003'] = int(statistics['YearStart'] < 2004)

    statistics.update({'Day{}'.format(k): v for k, v in stage_starts.items()})
    statistics['DayStart'] = statistics['DayWaiting']
    statistics['EvaluationDelay'] = stage_starts['Evaluating'] - stage_starts['Waiting']
    statistics['DetectionDelay'] = stage_starts['Detecting'] - stage_starts['Evaluating']
    statistics['DiagnosisDelay'] = stage_starts['Treating'] - stage_starts['Detecting']
    statistics['TreatmentPeriod'] = anc['TreatmentPeriod']
    statistics['Outcome'] = anc['Outcome'].name

    ro = list()
    for stage, ti in stage_starts.items():
        for obs in episode.Observations:
            if obs['Time'] == ti:
                ro.append(obs)
                break
        else:
            ro.append(episode.Observations[-1])

    for i, stage in enumerate(['Waiting', 'Evaluating', 'Detecting', 'Treating']):
        of = ro[i]
        ot = ro[i + 1]

        statistics[stage + 'Level'] = of['Level']
        if 'Sector' in of:
            statistics[stage + 'Sector'] = of['Sector']
        if 'InOut' in of:
            statistics[stage + 'InOut'] = of['InOut']
        statistics[stage + 'Visits'] = ot['Visits'] - of['Visits']
        statistics[stage + 'Patient_Cost'] = ot['Patient_Cost'] - of['Patient_Cost']
        statistics[stage + 'System_Cost'] = ot['System_Cost'] - of['System_Cost']

    stages = set([p['Stage'] for p in episode.Pathway])
    ts = set([h['Tre'] for h in episode.History])

    # post = set([h['Eva'] for h in episode.History if h['Time'] >= anc['TreatmentEnd']])

    statistics['Empirical'] = int('Empirical' in ts)
    statistics['InterruptedEvaluation'] = int(TBStage.IE in stages)
    statistics['TreatmentChange'] = int(TBStage.TC in stages)
    # statistics['PostCheck'] = int(len(post) > 1)

    return statistics


def find_arrival_timing(ctrl, episode):
    tr = episode.Attributes['DayTreating']

    for rec in episode.Records:
        if rec.Time is tr:
            hos = rec.Hospital
            break
    else:
        hos = episode.Records[-1].Hospital

    for rec in episode.Records:
        hv = ctrl.get_hospital(rec.Hospital)
        if hv['Anti-TB'] > 0:
            episode.Attributes['DayTreatmentAva'] = rec.Time
            break

    for rec in episode.Records:
        if rec.Hospital == hos:
            episode.Attributes['DayTreatmentHosp'] = rec.Time
            break
