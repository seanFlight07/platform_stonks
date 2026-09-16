import db
import api_fetcher
import transforms


def main():
    companies = db.get_active_companies()
    last_prices = db.get_last_prices()

    for company in companies:
        code = company["code"]
        exchange = company["exchange"]
        previous_close = last_prices.get(code)

        data = api_fetcher.api_fetch_stock(
            code,
            exchange
        )

        clean_data = transforms.transform_api_data(
            data,
            code,
            previous_close
        )
        print(clean_data)

if __name__ == "__main__":
    main()
