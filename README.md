# COMRADE

Canvassing & Organisation: Making Running Activism Downright Easy.

To use this, you'll need quite a lot of additional software.

#Installation

## PostgreSQL Database

It uses a recent PostgreSQL server, complete with PostGIS extension. Or SQLite, with the SpatiaLite extension.
I work with PostgreSQL. Install it.

```
sudo apt-get install postgresql-server-9.x-all postgresql-9.x-postgis-2.1 
```

Where x is the latest version of PostgreSQL available in the system repository.

Create your database user, then database "ssp_canvassing".

Enter the database

```
psql ssp_canvassing
```

then issue the command:

```
CREATE EXTENSION postgis;
```

This will install the postgis extensions you will need to use COMRADE.

## Virtualenv

I use virtualenvwrapper, but you can set up your environment or server as you see fit.

Enter your virtualenv, change to the project directory and use pip to install the python requirements.

```
pip install -r requirements/local.txt
```
or
```
pip install -r requirements/production.txt
```

## Web components

The COMRADE build process relies extensively on [npm](https://www.npmjs.com/) - the Node Package Manager.

This relies on the Foundation library, and the Leaflet map display library. I have included a bower.json file which will help.

Install bower:

```
npm install -g bower
```

Then install the client-side packages
```
bower install
```

## Build pipeline

I use grunt to build the JavaScript and CSS deliverables.

Install the dependencies (there's a package.json included):

```
npm install
```

And then type:

grunt

## Other data requirements

There are other data requirements.

Visit the [Ordnance Survey OpenData](https://www.ordnancesurvey.co.uk/opendatadownload/products.html) site and obtain the Code-Point® Open package.
This contains latitude and longitude data for every postcode in the country.

The postcode_locator "fill_up_db" script expects a CSV file with the fields "postcode","latitude" and "longitude". Save that as "postcodes.csv", and run the following:

```
./manage.py fill_up_db postcodes.csv
```