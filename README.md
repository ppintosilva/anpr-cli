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

```
