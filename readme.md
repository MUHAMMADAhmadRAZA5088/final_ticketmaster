# livenation
# create tmux
tmux
# livation folder directory path
cd /home/ubuntu/livenation/livenation_artist_data
# Activate virtual env
source /home/ubuntu/myenv/bin/activate 
# All JSON files will now be converted into empty JSON files.
python empty_json.py
# run livenation script
python livenation.py
# check a total session
tmux ls
# example 
0:------
1:------
# move the session
tmux a -t session_name
tmux a -t 0


# ticketmaster
# create tmux
tmux
# ticketmaster folder directory path
cd /home/ubuntu/ticketmaster/final_ticketmaster
# Activate virtual env
source /home/ubuntu/myenv/bin/activate 
# All JSON files will now be converted into empty JSON files.
python empty_json.py
# run ticketmaster script
python ticketmaster.py
# check a total session
tmux ls
# example 
0:------
1:------
# move the session
tmux a -t session_name
tmux a -t 0

# Data will be pulled from the AWS server to GitHub using that method.
# facevale folder directory path
cd /home/ubuntu/face_value_link
# remove all json files in this directory
rm ticketmaster_link.json
rm livenation_link.json
rm website_ticketmaster_link_livenation.json
rm website_ticketmaster_link_ticketmaster.json
# livation folder directory path
cd /home/ubuntu/livenation/livenation_artist_data
# This command will copy the ticketmaster_link.json, livenation_link.json  files from the specified source directory to the destination directory.
cp /home/ubuntu/livenation/livenation_artist_data/ticketmaster_link.json /home/ubuntu/face_value_link
cp /home/ubuntu/livenation/livenation_artist_data/livenation_link.json /home/ubuntu/face_value_link
# ticketmaster folder directory path
cd /home/ubuntu/ticketmaster/final_ticketmaster
# This command will copy the website_ticketmaster_link_livenation.json, website_ticketmaster_link_ticketmaster.json files from the specified source directory to the destination directory.
cp /home/ubuntu/ticketmaster/final_ticketmaster/website_ticketmaster_link_livenation.json /home/ubuntu/face_value_link
cp /home/ubuntu/ticketmaster/final_ticketmaster/website_ticketmaster_link_ticketmaster.json /home/ubuntu/face_value_link
# facevale folder directory path
cd /home/ubuntu/face_value_link
# Push all updated files to GitHub
git add .
git commit -m "link commit"
git push


# All the commands to pull from the AWS server to GitHub are written in run_move_file.sh
# run_move_file.sh
./run_move_file.sh

# get the link into personal computer
git clone "https://github.com/MUHAMMADAhmadRAZA5088/livenation_artist_link"

