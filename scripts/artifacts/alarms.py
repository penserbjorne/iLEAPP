import plistlib

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline


def get_alarms(files_found, report_folder, seeker):
    data_list = []

    for file_found in files_found:
        with open(file_found, "rb") as plist_file:
            pl = plistlib.load(plist_file)

            if 'MTAlarms' in pl:
                if 'MTAlarms' in pl['MTAlarms']:
                    for alarms in pl['MTAlarms']['MTAlarms']:
                        alarms_dict = alarms['$MTAlarm']

                        alarm_title = alarms_dict.get('MTAlarmTitle', 'Alarm')
                        fire_date = alarms_dict.get('MTAlarmFireDate', '')
                        dismiss_date = alarms_dict.get('MTAlarmDismissDate', '')

                        data_list.append((alarm_title, alarms_dict['MTAlarmEnabled'], fire_date, dismiss_date,
                                          alarms_dict['MTAlarmLastModifiedDate'], alarms_dict['MTAlarmRepeatSchedule'],
                                          alarms_dict['MTAlarmSound']['$MTSound']['MTSoundToneID'],
                                          alarms_dict['MTAlarmIsSleep'], alarms_dict['MTAlarmBedtimeDoNotDisturb'], ''))

                if 'MTSleepAlarm' in pl['MTAlarms']:
                    for sleep_alarms in pl['MTAlarms']['MTSleepAlarm']:
                        sleep_alarm_dict = pl['MTAlarms']['MTSleepAlarm'][sleep_alarms]

                        alarm_title = sleep_alarm_dict.get('MTAlarmTitle', 'Bedtime')

                        data_list.append((alarm_title, sleep_alarm_dict['MTAlarmEnabled'], sleep_alarm_dict['MTAlarmFireDate'],
                                          sleep_alarm_dict['MTAlarmDismissDate'], sleep_alarm_dict['MTAlarmLastModifiedDate'],
                                          sleep_alarm_dict['MTAlarmRepeatSchedule'], sleep_alarm_dict['MTAlarmSound']['$MTSound']['MTSoundToneID'],
                                          sleep_alarm_dict['MTAlarmIsSleep'], sleep_alarm_dict['MTAlarmBedtimeDoNotDisturb'],
                                          sleep_alarm_dict['MTAlarmBedtimeFireDate']))

    if len(data_list) > 0:
        report = ArtifactHtmlReport('Alarms')
        report.start_artifact_report(report_folder, 'Alarms')
        report.add_script()
        data_headers = ('Alarm Title', 'Alarm Enabled', 'Fire Date', 'Dismiss Date', 'Last Modified', 'Repeat Schedule', 'Alarm Sound', 'Is Sleep Alarm', 'Bedtime Not Disturbed', 'Bedtime Fire Date')
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()

        tsvname = 'Alarms'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = 'Alarms'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Alarms found')
