# Trainline Recap

A script to calculate stats about your trips booked on Trainline. WIP

## How to use

- Go to your past trips page on trainline : https://www.thetrainline.com/fr/my-account/bookings/past

- Inspect element on your browser and copy the inner HTML.

- Paste it in the file `input/trainline.html`

- Execute the script with 

  ```
  python main.py
  ```

  You will need the package `BeautifulSoup4` which can be installed with

  ```
  pip install beautifulsoup4
  ```

- Enter the distance of each trip when the script asks you

