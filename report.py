import argparse
import openpyxl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=str,
        help='path to excel file'
    )
    args = parser.parse_args()
    if args.file:
        file = args.file
    else:
        file = 'file.xlsx'
    book = openpyxl.open(file, read_only=True)

    sheet = book.active

    report_data = {}
    for row in range(2, sheet.max_row+1):
        asset = sheet[row][0].value
        target = sheet[row][1].value
        ip = sheet[row][2].value
        port = sheet[row][3].value
        scan_date = sheet[row][4].value
        severity = sheet[row][5].value
        score = sheet[row][6].value
        scanner = sheet[row][7].value
        vulnerabilityTypes = sheet[row][8].value
        CVE_id = sheet[row][9].value
        body = sheet[row][10].value
        wontFix = sheet[row][11].value
        falsePositive = sheet[row][12].value
        text = sheet[row][13].value
        ofExploits = sheet[row][14].value
        references = sheet[row][15].value
        if not report_data or not report_data[asset]:
            report_data[asset] = []
        report_data[asset].append({
            'target':target, 
            'ip':ip, 
            'port':port, 
            'scan_date':scan_date, 
            'severity':severity, 
            'score':score, 
            'scanner':scanner, 
            'vulnerabilityTypes':vulnerabilityTypes, 
            'CVE_id':CVE_id, 
            'body':body, 
            'wontFix':wontFix, 
            'falsePositive':falsePositive, 
            'text':text, 
            'ofExploits':ofExploits, 
            'references':references})
    for asset in report_data:
        with open(f'report_{asset}.html', 'w', encoding='utf8') as report_file:
            report_file.write(f'''<!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Report-{asset}</title>
            <style type="text/css">
                *{{
                    margin: 0;
                }}
                body{{
                    margin: 50px 50px 20px 50px;
                }}
                .res-title{{
                    color: blue;
                    text-align: center;
                }}
                .asset{{
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1 class="res-title">Scan Report {asset}</h1>
            </header>''')
            for row in report_data[asset]:
                #print(row)
                report_file.write(f'''<h2 class="asset">{row['target']}</h2>
                <h3 class="ip">{row['ip']}:{row['port']}</h3>
                <h3 class="severity">scan_date: {row['scan_date']}</h3>
                <h3 class="scanner">scanner: {row['scanner']}</h3>
                <p class="vulnerabilityTypes">VulnerabilityTypes: {row['vulnerabilityTypes']}</p>
                <p class="cveid">CVE: {row['CVE_id']}</p>
                <p class="cvss">{row['score']} - {row['severity']}</p>
                <p class="body">body: {row['body']}</p>
                <p class="wontFix">wontFix: {row['wontFix']}</p>
                <p class="falsePositive">falsePositive: {row['falsePositive']}</p>
                <p class="ofExploits">ofExploits: {row['ofExploits']}</p>
                <p class="ofExploits">Description: {row['text']}</p>
                <p class="references">references: {row['references']}</p>
            </body>
        </html>''')

if __name__=="__main__":
    main()