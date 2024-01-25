# AuraBotPOE

## Table of Contents
- [What it can do](#what-it-can-do)
- [Installation](#installation)
- [Usage](#usage)



## What it can do

<h3 align="center">
    This project is inspired by the popular game, Path of Exile.
</h3>

<p align="center">
    <img width="200" src="https://github.com/DiDawn/AuraBotPOE/assets/95550246/ce1fde18-0ccd-4259-a4d0-be880164e4a3" alt="POE logo">
</p>
In Path of Exile, players have the option to create a specialized character known as an "aura bot."
The essence of an aura bot is to focus on building a full support character that doesn't engage in
direct combat. Instead, the aura bot's primary role is to empower allies by stacking various area buffs,
commonly referred to as "auras."

<p align="center">
    <img width="400" src="https://github.com/DiDawn/AuraBotPOE/assets/95550246/622fd0d7-509b-4172-a39c-5a324bc782bc" alt="POE auras">
</p>

The term "aura" stend for a variety of buffs that enhance the stats of the entire team,
basically turning them close to invincible and greatly boosting their damage.
While the aura bot is has a very strong role in maximizing the team's potential,
the gameplay experience can be monotonous and less engaging for the player controlling the aura bot.
This is due to the fact that, as an aura bot, you aren't actively involved in direct combat. Youre just
standing there buffing everyone near you.

### Project Goal
The goal of this project is to automate the gameplay experience of an aura bot,
allowing players to enjoy the benefits of all the buffs without the need for manual control.


The bot will use image detection for automatic navigation his goal is pto follow the nearest person to stay by his side.


### Image detection
To achieve automatic navigation, the bot rely on [OpenCV](https://opencv.org/).
Users have the flexibility to choose between two methods of detection based on their preference:

#### 1-Custom Pre-trained Haar Cascade Classifier:

The bot can utilize a custom pre-trained cascade classifier.
This method is the faster one but sometime can be inaccurate. The accuracy of the model strongly depend on
the data-set used to train it. This one has been build with a couple of thousands images and is pretty accurate in 
all type of scenarios. However if you're not satisifed with his accuracy you can always switch to the second method:


#### 2-Template Matching:

Alternatively, users can opt for template matching if they find the classifier not performant enough. Keep in mind
that this method is slower.

#### What the bot is looking for
The bot focuses on the player's health/shield bar for consistency as 
it is the only element that does not vary 
between players


### Quick overview

#### Bot POV

Here you can see the prediction of the bot (standing in the middle).
If you look closely you can see the green rectangle around the player's health bar.
This is the area where the bot think the player's health bar is located.

https://github.com/DiDawn/AuraBotPOE/assets/95550246/fb98bc76-c03d-4f5d-8c43-02661b48ed20

#### Player POV

Here you can see the bot in action from the player's perspective.
The player is the one in the middle. The bot is the one running around him.

https://github.com/DiDawn/AuraBotPOE/assets/95550246/0aec11a0-c09d-4b5c-b7b9-e6bb0098b89b



## Installation
### Environment
If your main account is an aura bot, and you are simply bored by manually following others, you can skip to [the next part](#download-python).

If you want to run the aura bot on another account to support you while you're playing,
you will need to set up a new machine. Since you cannot run multiple instances of Steam on the same machine,
you will either need to use another PC or a virtual machine to run Path of Exile (POE).
(If you don't know how to set up a virtual machine, you can follow [this guide](https://techcommunity.microsoft.com/t5/educator-developer-blog/step-by-step-how-to-create-a-windows-11-vm-on-hyper-v-via/ba-p/3754100)).
Be sure to follow the instructions below on the machine where the bot will be run.

### Download python
If you do not have python installed yet, you can download it [here](https://www.python.org/downloads/). 

### Download the project
If you have git installed, you can clone the project by running the following command in your terminal:

```git clone https://github.com/DiDawn/AuraBotPOE.git```

If you do not have git installed, you can download the project [here](https://github.com/DiDawn/AuraBotPOE/zipball/master/).

### Install the required dependencies
To install the required dependencies, run the following command in your terminal:

```pip install -r requirements.txt```



## Usage

### In game settings

To ensure the bot works properly, you will need to adjust some settings in game.
To minimize the impact of rendering the game the bot as been trained on specific low video settings.
You will need to set all video settings to minimum in game if you want the bot to work properly.
You will also need to change the resolution to 800x600.
Make sure to run the game on full screen


### Start the bot

To start the bot you will need to have Path of Exile running on your machine.

Command to start the bot with default settings (make sure to past the full path of your file to replace "(path to the file)":

````python (path to the file)\app.py --classifier_name cascade.xml````

If you don't want to use the cascade classifier you can use this command instead:

````python (path to the file)\app.py --method template````

If you want to see custom settings you can type:

````python (path to the file)\app.py -help````


### Stop the bot

To stop the bot press "q".
