import argparse
from bot import Bot


def main():
    parser = argparse.ArgumentParser()

    detection_method_help = """Detection method to use.
    'cascade' for Haar Cascade detection
    'template' for template matching detection
    If you use 'cascade', you need to provide a classifier_name
    Default: 'classifier'"""
    parser.add_argument("--detection_method", type=str, default="classifier", help=detection_method_help)

    classifier_name_help = """Classifier name to use if detection_method is 'cascade'.
    The name must refer to the name of the cascade classifier you want to use in the cascade folder."""
    parser.add_argument("--classifier_name", type=str, default=None, help=classifier_name_help)

    scale_factor_help = "Scale factor to use. Should be between 1 and 10. Will scale down the image by this factor."
    parser.add_argument("--scale_factor", type=int, default=3, help=scale_factor_help)

    window_size_help = "Size of the window to capture. Should be the same as the game window. Default: (1920, 1080)"
    parser.add_argument("--window_size", type=int, nargs=2, default=(1920, 1080), help=window_size_help)

    grayscale_help = "If True, will convert the image to grayscale before searching for the health/shield bar."
    parser.add_argument("--grayscale", type=bool, default=False, help=grayscale_help)

    debug_mode_help = "If provided, should be 'visual_only', 'text_only' or 'all'. Will define what is displayed."
    parser.add_argument("--debug_mode", type=str, default=None, help=debug_mode_help)

    bar_priority_help = "Should be 'health' or 'shield'. Will define which one is searched first."
    parser.add_argument("--bar_priority", type=str, default='health', help=bar_priority_help)

    health_threshold_help = "Threshold of confidence for the health bar (only needed for 'template' method). Default: 0.85."
    parser.add_argument("--health_threshold", type=float, default=0.85, help=health_threshold_help)

    shield_threshold_help = "Threshold of confidence for the shield bar. Default: 0.85."
    parser.add_argument("--shield_threshold", type=float, default=0.85, help=shield_threshold_help)


    args = parser.parse_args()

    bot = Bot(args.detection_method, args.classifier_name, args.scale_factor, args.window_size, args.grayscale,
              args.debug_mode, args.bar_priority, args.health_threshold, args.shield_threshold)
    bot.start()


if __name__ == "__main__":
    main()
