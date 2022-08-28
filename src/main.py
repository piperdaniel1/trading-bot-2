from datatypes.PriceHistory import PriceHistory
from plot_helpers.ph_help import save_ph_plot

def main():
    print(" === Trading Bot 2 === ")
    ph = PriceHistory("MSFT", "1h", "30d")
    save_ph_plot(ph)
    
if __name__ == '__main__':
    main()