# Fire_fighting_bot_simulation_in-gazebo_using-feedback_from_lidar
### Description: 
A mobile robot with 3-R manipulator which can be teleoperated to extinguish fire. When it reaches the premises of fire, it will keep a 2m distance from the zone of hazard and the nozzle will point in that direction and extinguish the fire. Everything was designed from scratch, URDF, controller definition, teleoperation, and then automating it using a publisher script. In the gazebo simulation environment, walls were assumed to be fire, so a safe zone was defined which was 2 m away from the walls. So, basically, you can teleoperate the bot to the location of the fire, the moment it senses the wall(fire), it gave feedback about the red zone and the bot will take command over the teleoperation. It first will move at least 2 m away from the fire zone, and then points the nozzle (end effector) towards the fire, for a definite time and then again will give you the feedback once the fire is doused. The detection system was achieved by subscribing to the lidar topic, and callback function of the subscriber.


METHOD TO RUN THE PACKAGE
### Step 1: 
Extract the folder 'Fire_fighting_bot-main' and copy the folder 'fire_fight_1', which is inside src, to your catkin_ws/src
### Step 2: Build the Package. 
 In your terminal go to your catkin_ws folder and type 
 #### catkin_make clean && catkin_make
 Note: Source your catkin workspace (e.g. if catkin_ws is in your home directory, do source ~/catkin_ws/devel/setup.bash)
 optional: add this command to your .bashrc
### Step 3: Launch the package
 After sourcing the ~/.bashrc, type 
 #### roslaunch fire_fight_1 template_launch.launch
 This will spawn the robot in Gazebo.
### Step 4: Running the teleop
 Open a new terminal and type 
   #### source /opt/ros/noetic/setup.bash
   #### source ~/catkin_ws/devel/setup.bash
   #### rosrun fire_fight_1 teleop.py
  If the above command does not work, it is mostly because teleop.py is not an executable.
  Alternative: To make teleop.py an executable. Go to catkin_ws/src/fire_fight_1/src , and type 
   #### chmod +x teleop.py
   Repeat from Step 2.

Now, the teleop is running and you can press the mentioned keys to control the robot.
