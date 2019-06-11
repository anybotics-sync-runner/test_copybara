#!/usr/bin/env python
import em
import os
import argparse
import sys

TEMPLATE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_EXTENSION='.em'
WORKFLOW_UPDATE_MASTER='update_master'
WORKFLOW_IMPORT_PR='import_pr'

class CopybaraSubsitutions:
    def __init__(self, project, workflow):
        self.project = project
        self.workflow = workflow

        self.destination_url = None
        self.origin_url = None

        self.origin_paths = '["**"]'
        self.origin_excludes = "[]"
        self.destination_paths = '["**"]'
        self.destination_excludes = "[]"

        self.default_author = "Ghost User <ghost@example.com>"
        self.transformations = None

def createCopybaraFile(substitutions, working_dir, template_dir, force):
    # Substitute
    subs = substitutions.__dict__;

    # Create directory
    directory = working_dir + "/" + substitutions.workflow + "/" + substitutions.project
    if os.path.isdir(directory):
        if not force:
            print("Folder {0} already exists. Use --force flag to generate files anyway.".format(directory))
            sys.exit()
    else:
        os.makedirs(directory)


    # Expand template
    template_file = template_dir + "/copybara_template_" + substitutions.workflow + TEMPLATE_EXTENSION;
    with open(template_file, 'r') as fh:
        result = em.expand(fh.read(), **subs)

    # Write the result
    copybara_file = directory + "/copy.bara.sky"
    with open(copybara_file, 'w') as f:
        f.write(result)


def getAnymalResearchOriginPaths():
    return '"drivers/depth_sensors/actuated_lidar/**",\n\
            "tools/any_common/**",\n\
            "simulation/any_gazebo/**",\n\
            "user_interface/any_joy/**",\n\
            "tools/ros/any_node/**",\n\
            "tools/any_utils/**",\n\
            "tools/ros/any_utils_ros/**",\n\
            "anydrive/anydrive_sdk/**",\n\
            "anymal/anymal/**",\n\
            "anymal/anymal_b/anymal_b/**",\n\
            "motion_control/controllers/anymal_ctrl_dynamic_gaits/**",\n\
            "motion_control/controllers/anymal_ctrl_staticwalk/**",\n\
            "motion_control/controllers/anymal_ctrl_test/**",\n\
            "motion_control/controllers/anymal_ctrl_trot/**",\n\
            "motion_control/highlevel_controller/anymal_highlevel_controller/**",\n\
            "drivers/anymal_drivers/anymal_lowlevel_controller/**",\n\
            "anymal/anymal_navigation/**",\n\
            "perception/state_estimation/anymal_state_estimator/**",\n\
            "infrastructure/development/clang_tools/**",\n\
            "tools/modelling/collisions/**",\n\
            "perception/state_estimation/contact_estimation/**",\n\
            "tools/communication/cosmo/**",\n\
            "tools/trajectory_generation/curves/**",\n\
            "tools/trajectory_generation/signal_generation/**",\n\
            "drivers/actuators/dynamixel/**",\n\
            "drivers/actuators/dynamixel_motor/**",\n\
            "perception/elevation_mapping/**",\n\
            "motion_control/free_gait/**",\n\
            "motion_control/controllers/free_gait_anymal/**",\n\
            "simulation/gazebo2rviz/**",\n\
            "tools/data_structure/grid_map/**",\n\
            "simulation/hector_gazebo/**",\n\
            "perception/icp_tools/**",\n\
            "tools/modelling/kindr/**",\n\
            "tools/modelling/kindr_ros/**",\n\
            "drivers/actuators/libdynamixel/**",\n\
            "perception/state_estimation/lightweight_filtering/**",\n\
            "perception/state_estimation/lightweight_filtering_models/**",\n\
            "perception/localization_manager/**",\n\
            "motion_control/loco/**",\n\
            "motion_control/controllers/locomotion_planner/**",\n\
            "tools/logging/message_logger/**",\n\
            "motion_control/motion_generation/**",\n\
            "tools/optimization/numopt/**",\n\
            "tools/optimization/osqp/**",\n\
            "tools/optimization/qdldl/**",\n\
            "tools/parameter_handler/**",\n\
            "tools/point_cloud_processing/point_cloud_processing/**",\n\
            "tools/point_cloud_processing/pointmatcher-ros/**",\n\
            "simulation/pysdf/**",\n\
            "anymal/quadruped_common/**",\n\
            "tools/modelling/rbdl/**",\n\
            "motion_control/robot_measurements/**",\n\
            "tools/robot_utils/**",\n\
            "motion_control/highlevel_controller/roco/**",\n\
            "motion_control/highlevel_controller/rocoma/**",\n\
            "tools/modelling/romo/**",\n\
            "drivers/anymal_drivers/rpsm_software/**",\n\
            "anydrive/series_elastic_actuator/**",\n\
            "tools/logging/signal_logger/**",\n\
            "perception/state_estimation/two_state_information_filter/**",\n\
            "user_interface/user_interface/**",\n\
            "motion_control/whole_body_control/**",\n\
            "anymal/anymal_b/anymal_b_drivers/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_bany/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_bear/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_bedi/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_bonnie/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_boxy/**",\n\
            "anymal/anymal_b/anymal_b_robots/anymal_bunny/**",\n\
            "tools/state_machine/conditional_state_machine/**",\n\
            "drivers/depth_sensors/depth_sensor_calibration/**",\n\
            "drivers/remote_controls/hri-safe-remote-control-system/**",\n\
            "drivers/depth_sensors/librealsense/**",\n\
            "tools/ethercat/openethercat_soem/**",\n\
            "drivers/depth_sensors/realsense/**",\n\
            "drivers/gps/ethz_piksi_ros/**",\n\
            "drivers/imus/xsensmt/**"'

def getAnymalResearchExcludePaths():
    return '"anymal/quadruped_common/battery_monitoring/**"'

def createAnymalResearch(args):
    substitutions = CopybaraSubsitutions("anymal_research", args.workflow)

    if args.workflow == WORKFLOW_UPDATE_MASTER:
        substitutions.origin_url = args.anybotics_url;
        substitutions.destination_url = args.anymal_research_url;
        substitutions.origin_paths = "[" + getAnymalResearchOriginPaths() + "]"
        substitutions.origin_excludes = "[" + getAnymalResearchExcludePaths() + "]"
    elif args.workflow == WORKFLOW_IMPORT_PR:
        substitutions.origin_url = args.anymal_research_url;
        substitutions.destination_url = args.anybotics_url;
        substitutions.destination_paths = "[" + getAnymalResearchOriginPaths() + "]"

    createCopybaraFile(substitutions, args.working_dir, args.template_dir, args.force)

def createAnyboticsGithub(repo, path_in_monorepo, args):
    substitutions = CopybaraSubsitutions(repo, args.workflow)
    github_url = "git@github.com:ANYbotics/" + repo + ".git"

    if args.workflow == WORKFLOW_UPDATE_MASTER:
        substitutions.origin_url = args.anybotics_url;
        substitutions.destination_url = github_url
        substitutions.origin_paths = '["' + path_in_monorepo + repo +  '/**"]'
        substitutions.transformations = 'core.move("' + path_in_monorepo + repo + '", ""),'
    elif args.workflow == WORKFLOW_IMPORT_PR:
        substitutions.origin_url = github_url
        substitutions.destination_url = args.anybotics_url;
        substitutions.destination_paths = '["' + path_in_monorepo + repo +  '/**"]'
        substitutions.transformations = 'core.move("", "' + path_in_monorepo + repo + '"),\n\
                                        metadata.expose_label("COPYBARA_INTEGRATE_REVIEW"),\n\
                                        metadata.expose_label("GITHUB_PR_NUMBER", new_name ="Closes", separator=" #"),\n\
                                        metadata.replace_message("BEGIN_PUBLIC\\n${COPYBARA_CURRENT_MESSAGE}\\nEND_PUBLIC"),'

    createCopybaraFile(substitutions, args.working_dir, args.template_dir, args.force)

def main():

    parser = argparse.ArgumentParser(description="Create copybara files from a template for a given workflow. Template must be named copybara_template_ + workflow + .em.")
    parser.add_argument("workflow", help="Workflow name (update_master, import_pr)", type=str, choices=[WORKFLOW_IMPORT_PR, WORKFLOW_UPDATE_MASTER])
    parser.add_argument("--anymal-research-url", help="URL of ANYmal Research repository.", type=str, default="git@code.anymal.com:anymal_research/anymal_research.git")
    parser.add_argument("--anybotics-url", help="URL of ANYbotics repository.", type=str, default="git@git.anybotics.com:anybotics/anybotics.git")
    parser.add_argument("--working-dir", help="Working directory in which to create folders with copybara files.", type=str, default=os.getcwd())
    parser.add_argument("--template-dir", help="Directory in which the template files are located.", type=str, default=TEMPLATE_PATH)
    parser.add_argument("-f", "--force", help="Force overwriting existing folders.", action="store_true")
    args = parser.parse_args()

    createAnymalResearch(args)

    createAnyboticsGithub("anymal_b_simple_description", "anymal/anymal_b/", args)
    createAnyboticsGithub("ar_track_alvar", "tools/image_processing/", args)
    createAnyboticsGithub("curves", "tools/trajectory_generation/", args)
    createAnyboticsGithub("elevation_mapping", "perception/", args)
    createAnyboticsGithub("ethz_piksi_ros", "drivers/gps/", args)
    createAnyboticsGithub("gazebo2rviz", "simulation/", args)
    createAnyboticsGithub("gnome-shell-ping-monitor-applet", "user_interface/", args)
    createAnyboticsGithub("grid_map", "tools/data_structure/", args)
    createAnyboticsGithub("kindr", "tools/modelling/", args)
    createAnyboticsGithub("kindr_ros", "tools/modelling/", args)
    createAnyboticsGithub("libnabo", "tools/data_structure/", args)
    createAnyboticsGithub("libpointmatcher", "tools/point_cloud_processing/", args)
    createAnyboticsGithub("libuvc", "drivers/depth_sensors/", args)
    createAnyboticsGithub("linuxdeployqt", "infrastructure/deployment/", args)
    createAnyboticsGithub("nmea_navsat_driver", "drivers/gps/", args)
    createAnyboticsGithub("point_cloud_io", "tools/point_cloud_processing/", args)
    createAnyboticsGithub("pointmatcher-ros", "tools/point_cloud_processing/", args)
    createAnyboticsGithub("pysdf", "simulation/", args)
    createAnyboticsGithub("rqt_multiplot_plugin", "user_interface/", args)
    createAnyboticsGithub("siitool", "tools/ethercat/", args)
    createAnyboticsGithub("variant", "user_interface/", args)

    createAnyboticsGithub("any_ping_indicator", "user_interface/", args)
    createAnyboticsGithub("catkin_create_rqt", "infrastructure/development/", args)
    createAnyboticsGithub("dynamixel_motor", "drivers/actuators/", args)
    createAnyboticsGithub("free_gait", "motion_control/", args)
    createAnyboticsGithub("hri-safe-remote-control-system", "drivers/remote_controls/", args)
    createAnyboticsGithub("librealsense", "drivers/depth_sensors/", args)
    createAnyboticsGithub("osqp", "tools/optimization/", args)
    createAnyboticsGithub("qdldl", "tools/optimization/", args)
    createAnyboticsGithub("realsense", "drivers/depth_sensors/", args)
    createAnyboticsGithub("two_state_information_filter", "perception/state_estimation/", args)

    createAnyboticsGithub("anydistro", "infrastructure/deployment/", args)
    createAnyboticsGithub("any_node", "tools/ros/", args)
    createAnyboticsGithub("message_logger", "tools/logging/", args)
    createAnyboticsGithub("parameter_handler", "tools/", args)
    createAnyboticsGithub("roco", "motion_control/highlevel_controller/", args)
    createAnyboticsGithub("rocoma", "motion_control/highlevel_controller/", args)
    createAnyboticsGithub("rocoma_example", "motion_control/highlevel_controller/", args)
    createAnyboticsGithub("signal_logger", "tools/logging/", args)

if __name__== "__main__":
    main()
