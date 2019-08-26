# anpr-cli
A CLI for pre-processing and analysing batches of ANPR data

## Pipeline

```bash
# Wrangle raw cameras csv dataset
anpr wrangle cameras \
  --names "id,name,description,lat,lon,is_commissioned,type,operating_since" \
  --skip-lines 1 \
  data/raw_cameras.csv data/wrangled_cameras.geojson

# Get network from camera locations
anpr wrangle network \
  --figures \
  --dpi 80 \
  data/wrangled_cameras.geojson data/raw_network.pkl

# Merge network and cameras into a single graph
anpr wrangle merge \
  --figures \
  --dpi 80 \
  data/wrangled_cameras.geojson data/raw_network.pkl data/merged_network.pkl

# Compute valid camera-pairs
anpr wrangle camera-pairs \
  data/merged_network.pkl data/camera-pairs.csv

# Wrangle nodes
anpr wrangle nodes \
  --names "id,name,description,lat,lon" \
  --skip-lines 1 \
  data/raw_nodes.csv data/wrangled_cameras.geojson data/wrangled_nodes.geojson

# Get 'expert camera-pairs' from links and wrangled nodes
anpr wrangle expert-pairs \
 data/raw_links.csv data/wrangled_nodes.geojson data/expert-pairs.csv

# Wrangle one raw anpr csv file
anpr wrangle raw-anpr \
  --confidence-threshold 70.0 \
  --cameras-geojson data/wrangled_cameras.geojson \
  --names "vehicle,camera,timestamp,confidence" \
  --skip-lines 0 \
  data/NPDATA.csv data/wrangled_NPDATA.pkl

anpr compute trips \
  --max-speed 120.0 \
  --duplicate-threshold 150.0 \
  --speed-threshold 3.0 \
  data/wrangled_NPDATA.pkl data/camera-pairs.csv data/trips_NPDATA.pkl

anpr compute flows \
  --freq "5T" \
  --output-format "csv" \
  --single-precision \
  data/trips_NPDATA.pkl data/flows_NPDATA.csv

```
