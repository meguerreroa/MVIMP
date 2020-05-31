"""
Input: A single video file;
Output: A single inserted video file.
"""

from mvimp_utils.location import *
import torch
from mvimp_utils.ffmpeg_helper import *
from mvimp_utils.file_op_helper import *
import argparse

torch.backends.cudnn.benchmark = True


def config():
    parser = argparse.ArgumentParser(description="Inference DAIN.")
    parser.add_argument(
        "--time_step",
        "-ts",
        type=float,
        default=0.5,
        choices=[0.5, 0.25, 0.125],
        help="Choose the time steps, time step must be one of 0.5/0.25/0.125.",
    )
    parser.add_argument(
        "--high_resolution",
        "-hr",
        action="store_true",
        help="split the frames when handling 720+ videos",
    )
    return parser.parse_args()


if __name__ == "__main__":
    os.chdir(DAIN_PREFIX)
    print(f"Current PyTorch version is {torch.__version__}")
    args = config()

    # STAGE 0: handling input videos
    input_videos_list = os.listdir(input_data_dir)
    file_transfer(input_data_dir, tmp_data_dir)
    clean_folder(input_data_dir)
    for video_file in input_videos_list:

        # STAGE 1: video pre-processing
        video_file_link = os.path.join(tmp_data_dir, video_file)
        frame_num = frames_info(video_file_link)
        assert (
            frame_num >= 2
        ), "You need more than 2 frames in the video to generate insertion."
        fps = fps_info(video_file_link)
        target_fps = float(fps) / args.time_step
        video_extract(src=video_file_link, dst=input_data_dir, thread=4)
        # More aggressively exclude possible errors
        print(
            f"\n--------------------SUMMARY--------------------\n"
            f"Current input video file is {video_file},\n"
            f"{video_file}'s fps is {fps},\n"
            f"{video_file} has {frame_num} frames.\n"
            f"Now we will process this video to {target_fps} fps.\n"
            f"Frame split method will {'be' if args.high_resolution else 'not be'} used.\n"
            f"--------------------NOW END--------------------\n\n"
        )

        # STAGE 2: Inference
        cmd = (
            f"python3 -W ignore vfi_helper.py "
            f"--src {input_data_dir} "
            f"--dst {output_data_dir} "
            f"--time_step {args.time_step} "
            f"{'--high_resolution' if args.high_resolution else ''} "
        )
        print(cmd)
        os.system(cmd)

        # STAGE 3: video post-processing
        os.chdir(DAIN_PREFIX)
        clean_folder(input_data_dir)
        file_order(src=output_data_dir, dst=input_data_dir)
        output_video_file = f"{args.input_video.split('.')[0]}-{target_fps}.{args.input_video.split('.')[1]}"

        video_fusion(
            src=input_data_dir + "/%10d.png",
            dst=os.path.join(tmp_data_dir, output_video_file),
            fps=target_fps,
            thread=4,
        )
        clean_folder(input_data_dir)
        clean_folder(output_data_dir)

    file_transfer(tmp_data_dir, output_data_dir)
    clean_folder(tmp_data_dir)
