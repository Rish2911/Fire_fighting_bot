# Fire_fighting_bot_simulation_in-gazebo_using-feedback_from_lidar
### Description: 
A mobile robot with 3-R manipulator which can be teleoperated to extinguish fire. When it reaches the premises of fire, it will keep a 2m distance from the zone of hazard and the nozzle will point in that direction and extinguish the fire.

### Step 1: 
Extract the folder 'Fire_fighting_bot_simulation_in-gazebo_using-feedback_from_lidar-main' and copy the folder 'fire_fight_1', which is inside src, to your catkin_ws/src
### Step 2: Build the Package. 
 In your terminal go to your catkin_ws folder and type 
 #### catkin_make clean && catkin_make
 Note: Source ~/.bashrc 
### Step 3: Launch the package
 After sourcing the ~/.bashrc, type 
 #### roslaunch fire_fight_1 template_launch.launch
 This will spawn the robot in Gazebo.
### Step 4: Running the teleop
 Open a new terminal and type 
   #### source /opt/ros/noetic/setup.bash
   #### source ~/catkin_ws/devel/setup.bash
   #### rosrun fire_fight_1 lidar.py
  If the above command does not work, it is mostly because lidar.py is not an executable.
  Alternative: To make lidar.py an executable. Go to catkin_ws/src/fire_fight_1/src , and type 
   #### chmod +x lidar.py
   Repeat from Step 2.

Now, the teleop is running and you can press the mentioned keys to control the robot.
