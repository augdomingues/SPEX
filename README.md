# SPEX
Stay Point EXtractor


usage: spex.py [-h] --action {extract_points,extract_metrics,extract_both}
               [-t [T]] [-d [{haversine,euclidean}]] [-r [R]]
               filename output_location

SPEX: Stay Point EXtractor.

positional arguments:
  filename              Trace file name
  output_location       Output folder location

optional arguments:
  -h, --help            show this help message and exit
  --action {extract_points,extract_metrics,extract_both}
                        Choose what action to do.
  -t [T]                Time threshold (in minutes)
  -d [{haversine,euclidean}]
                        Distance function (haversine or euclidean)
  -r [R]                Radius threshold (in meters)


## Usage examples

python spex.py my_trace.csv my_output_folder/ --action extract_both
(Extract the stay points and the metrics from the my_trace.csv file and store the stay points in the my_output_folder, using the default values of time threshold (30 minutes), radius threshold (500 meters) and distance function (haversine)

python spex.py my_trace.csv my_output_folder/ --action extract_metrics
(Extract only the metrics)

python spex.py my_trace.csv my_output_folder/ --action extract_points -t 60 -d euclidean -r 1000
(Extracts only the stay points and sets specific values for time, radius and distance function)



