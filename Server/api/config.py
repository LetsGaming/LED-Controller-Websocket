start_animations = {
    'white': {
        'name': 'White',
        'animation_name': 'white',
        'description': 'Sets the complete LED-Strip to white',
        'args': []
    },
    'custom_color': {
        'name': 'Custom Color',
        'animation_name': 'custom_color',
        'description': 'Sets the color of the complete LED Strip',
        'args': ['red', 'green', 'blue']
    },
    'custom_fill': {
        'name': 'Custom Fill',
        'animation_name': 'custom_fill',
        'description': 'Fills a certain amount of the pixels with a given color',
        'args': ['red', 'green', 'blue', 'percentage']
    }
}

standard_animations = {
    'rainbow_cycle': {
        'name': 'Rainbow Cycle',
        'animation_name': 'rainbow_cycle',
        'description': 'Smoothly transitions colors in a cyclical pattern resembling a rainbow.',
        'args': []
    },
    'rainbow_comet': {
        'name': 'Rainbow Comet',
        'animation_name': 'rainbow_comet',
        'description': 'Simulates a comet-like trail of rainbow colors.',
        'args': []
    },
    'theater_chase_rainbow': {
        'name': 'Theater Chase Rainbow',
        'animation_name': 'theater_chase_rainbow',
        'description': 'Produces a theater chase effect with a rainbow of colors.',
        'args': []
    },
    'rainbow_bounce': {
        'name': 'Rainbow Bounce',
        'animation_name': 'rainbow_bounce',
        'description': 'Bounce a rainbow color back and forth across the LED strip.',
        'args': [],
    },
    'random_bounce': {
        'name': 'Random Bounce',
        'animation_name': 'random_bounce',
        'description': 'Bounce a random color back and forth across the LED strip.',
        'args': [],
    },
}

custom_animations = {
    'custom_rainbow_cycle': {
        'name': 'Custom Rainbow Cycle',
        'animation_name': 'custom_rainbow_cycle',
        'description': 'Draw rainbow that uniformly distributes itself across all pixels.',
        'args': ['colors'],
    },
    'color_wipe': {
        'name': 'Color Wipe',
        'animation_name': 'color_wipe',
        'description': 'Wipes the LED strip with a single color, creating a visually striking effect.',
        'args': ['red', 'green', 'blue']
    },
    'theater_chase': {
        'name': 'Theater Chase',
        'animation_name': 'theater_chase',
        'description': 'Creates a theater chase effect with custom colors.',
        'args': ['red', 'green', 'blue']
    },
    'strobe': {
        'name': 'Strobe',
        'animation_name': 'strobe',
        'description': 'Produces a strobe effect using custom colors.',
        'args': ['red', 'green', 'blue']
    },
    'color_chase': {
        'name': 'Color Chase',
        'description': 'Generates a chasing effect with custom colors.',
        'args': ['red', 'green', 'blue']
    },
}

special_animations = {
    'blink': {
        'name': 'Blink',
        'animation_name': 'blink',
        'description': 'Repeatedly blinks the LED strip with a specified color combination.',
        'args': ['red', 'green', 'blue', 'blinking_speed']
    },
    'fade': {
        'name': 'Fade',
        'animation_name': 'fade',
        'description': 'Gradually fades the LED strip from one color to another.',
        'args': ['from_red', 'from_green', 'from_blue', 'to_red', 'to_green', 'to_blue', 'steps', 'fading_speed']
    },
    'sparkle': {
        'name': 'Sparkle',
        'animation_name': 'sparkle',
        'description': 'Adds sparkling effects to the LED strip by randomly illuminating individual LEDs.',
        'args': ['red', 'green', 'blue', 'sparkle_count']
    },
    'scanner_effect': {
        'name': 'Scanner Effect',
        'animation_name': 'scanner_effect',
        'description': 'Creates a scanning effect by moving a single colored pixel back and forth.',
        'args': ['red', 'green', 'blue', 'scan_speed', 'tail_length']
    },
    'yoyo_theater': {
        'name': 'Yoyo Theater',
        'animation_name': 'yoyo_theater',
        'description': 'Creates a yoyo-like effect and lets the string colors bounce around',
        'args': ['red', 'green', 'blue', 'yoyo_speed']
    },
    'breathing_effect': {
        'name': 'Breathing Effect',
        'animation_name': 'breathing_effect',
        'description': 'Create a breathing effect by gradually changing the brightness of the color.',
        'args': ['red', 'green', 'blue', 'breathing_duration']
    },
    'color_ripple': {
        'name': 'Color Ripple',
        'animation_name': 'color_ripple',
        'description': 'Create a ripple effect with a changing color.',
        'args': ['red', 'green', 'blue', 'ripple_speed'],
    },
}
