from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def main():
    with open("input/trainline.html", encoding="utf8") as f:
        soup = BeautifulSoup(f, "html.parser")

    try:
        with open("input/distances.txt", encoding="utf8") as f:
            distances = dict()
            for l in f.readlines():
                if l.startswith("departure"):
                    continue
                splitted = l.strip().split(";")
                distances[(splitted[0], splitted[1])] = int(splitted[2])
    except FileNotFoundError:
        distances = dict()
    trip_div_class = "_19i317l"
    trip_div = soup.find_all("div", class_=trip_div_class)
    trips = []
    for trip in trip_div:
        trip_text = trip.get_text().strip()
        splitted = trip_text.splitlines()
        locations = splitted[0]
        destination = locations.split(" — ")[1]
        departure = locations.split(" — ")[0]
        if len(splitted) == 2:
            price = float(splitted[1].replace("€", "").strip().replace(",", "."))
        else:
            price = 0
        trips.append((departure, destination, price))

    trip_div_v2 = "_f3xnejb"
    duration_div = "_oigb65"
    trips_v2 = []
    for trip in soup.find_all("div", class_=trip_div_v2):
        trip_div = trip.find("div", class_=trip_div_class)
        trip_text = trip_div.get_text().strip()
        splitted = trip_text.splitlines()
        locations = splitted[0]
        destination = locations.split(" — ")[1]
        departure = locations.split(" — ")[0]
        if len(splitted) == 2:
            price = float(splitted[1].replace("€", "").strip().replace(",", "."))
        else:
            price = 0
        duration_str = trip.find("span", class_=duration_div).get_text().strip()
        duration_str = duration_str.split(", ")[0]
        if 4 <= len(duration_str) <= 6:
            duration = timedelta(minutes=int(duration_str[:-3]))
        else:
            t = datetime.strptime(duration_str, "%Hh %Mmin")
            duration = timedelta(hours=t.hour, minutes=t.minute)
        trips_v2.append((departure, destination, price, duration))

    total_distance = 0
    total_price = 0
    total_time = timedelta()
    
    for trip in trips_v2:
        departure = trip[0]
        destination = trip[1]
        price = trip[2]
        duration = trip[3]
        if price == 0:
            print(f"Price not found for {departure} to {destination}, cancelled ?")
            continue
        if (departure, destination) not in distances:
            if (destination, departure) in distances:
                d = distances[(destination, departure)]
            else:
                d = int(input(f"Distance from {departure} to {destination} : "))
            distances[(departure, destination)] = d
        total_distance += distances[(departure, destination)]
        total_price += price
        total_time += trip[3]
        print(f"> {departure} - {destination} : {duration}")
        print(
            f"   Average speed of the trip : {distances[(departure, destination)] / trip[3].seconds * 3600:.0f} km/h"
        )
    print("\n-----------------------\nSummary :")
    print(f"Number of trips: {len(trips)}")
    print(f"Total distance: {total_distance} km")
    print(f"Total price: {total_price:.2f} €")
    print(f"Price per km: {total_price / total_distance:.2f} €/km")
    print(f"Total time: {total_time}")
    print(
        f"Average speed: {total_distance / (total_time.days * 24 * 60 * 60 + total_time.seconds) * 3600:.0f} km/h"
    )
    write_distances_file(distances)


def write_distances_file(distances):
    with open("input/distances.txt", "w", encoding="utf8") as f:
        f.write("departure;destination;distance\n")
        for k, v in distances.items():
            f.write(f"{k[0]};{k[1]};{v}\n")


if __name__ == "__main__":
    main()
