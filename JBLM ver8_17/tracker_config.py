# QSettings configurations
ORGANIZATION_NAME = "polarityAI"
APPLICATION_NAME = "JBLM_ver8_16"
# log file name
LOG_FILE = 'JBLM_ver8_16.log'
# directory
PRINGLES = 'JBLM_ver8_16'
# ditfitty
DATEFORMAT = '%d-%b-%y %I:%M:%S %p'
FILE_MODE = 'w'
# for when's ya at the home local. ;)
# DB_NAME = 'theDBofTracksAugust8th.db'
DB_NAME = 'theDBofTracksAugust8th.db'


COLOR = "color:rgb(255,255,255);font-weight:500;font-size:9pt;"
COLOR2 = "color:rgb(255,255,255);font-weight:bold;font-size:9pt;"
STYLESHEET = """
#sun_date {font-weight:bold; font-size:10pt; color:rgb(230, 77, 60);}
#mon_date {font-weight:bold; font-size:10pt; color:rgb(236, 77, 114);}
#tues_date {font-weight:bold; font-size:10pt; color:rgb(222, 94, 160);}
#wed_date {font-weight:bold; font-size:10pt; color:rgb(193, 118, 194);}
#thurs_date {font-weight:bold; font-size:10pt;color:rgb(157, 139, 212);}
#fri_date {font-weight:bold; font-size:10pt; color:rgb(127, 154, 214);}
#sat_date {font-weight:bold; font-size:10pt; color:rgb(115, 165, 204);}
"""
LILY_APP = 'JBLM_LILY_MODULE'
AGENDA_NAME = 'JBLM_AGENDA_MODULE'

COURSEWORK = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Day at a Glance</title>
<style>
    table {
        border:1px solid #121212;
    }
    th, td {
/*        margin: 2px 4px;*/
        border:1px solid #121212;
        padding: 4px 4px 4px 4px;
        border-radius:8px;
        text-align: left;
    }
</style>
</head>
<body>
<table>
    <tr>
        <td></td>
    </tr>
</table>
</body>
</html>
"""

INJECT_IMPORTANCE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Day at a Glance</title>
<style>
    table {
        background:rgba(90,90,90,0.3);
        border:none;
    }
    th, td {
/*        margin: 2px 4px;*/
        border: 1px solid rgba(100,100,200, 0.4);
        padding: 4px 22px 2px 22px;
        text-align: left;
    }
</style>
</head>
<body>
<h4>important<sub>things</sub><sup>COME</sup></h4>
<br>

</body>
</html>
"""

DELAY_INJECT = """
<table>
    <tr>
        <th>
            <strong>Time</strong>
        <th>
        <th style="width:100%">
            <strong>Task</strong>
        <th>
    </tr>
    <tr>
        <td><strong></strong></td>
        <td></td>
    </tr>
        <tr>
        <td><strong></strong></td>
        <td></td>
    </tr>
        <tr>
        <td><strong></strong></td>
        <td></td>
    </tr>

"""

INJECT_TABLE_ONE = """
<style>
    table {
        border:1px solid #121212;
    }
    th, td {
/*        margin: 2px 4px;*/
        border:1px solid #121212;
        padding: 4px 4px 4px 4px;
        border-radius:8px;
        text-align: left;
    }
</style>
<table>
    <tr>
        <th>
            Head
        </th>
        <th>
            Head
        </th>
    </tr>
    <tr>
        <td>

        </td>
        <td>

        </td>
    </tr>
    <tr>
        <td>

        </td>
        <td>

        </td>
    </tr>
    <tr>
        <td>

        </td>
        <td>

        </td>
    </tr>
    <tr>
        <td>

        </td>
        <td>

        </td>
    </tr>
"""
