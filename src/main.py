import inquirer
from ticker_details import execute_ticker_details

def main():
    print(" === Trading Bot 2 === ")
    options = [
        inquirer.List('program',
                    message='Which program do you want to launch?',
                    choices=['Ticker Details'],
        ),
    ]

    answer = inquirer.prompt(options)
    if answer['program'] == 'Ticker Details':
        execute_ticker_details()
    #print(yf.Ticker("MSFT").info)

if __name__ == '__main__':
    main()