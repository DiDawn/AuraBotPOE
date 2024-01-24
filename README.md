# AuraBotPOE

## Table of Contents
- [What it can do](#what-it-can-do)
- [Installation](#installation)
- [Usage](#usage)
- [Train your own cascade classifier](#train-your-own-model)



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


The bot will employs image detection for automatic navigation. It will follow the nearest person constantly
trying stand by his side.


### Image detection
To achieve automatic navigation, the bot rely on [OpenCV](https://opencv.org/).
Users have the flexibility to choose between two methods of detection based on their preference:

#### 1-Custom Pre-trained Haar Cascade Classifier:

The bot can utilize a custom pre-trained cascade classifier.
This method is the faster one but sometime can be inaccurate. The accuracy of the model strongly depend on
the data-set used to train it. This one has been build with a couple of thousands images and is pretty accurate in 
all type of scenarios. If you find it not accurate enough and find the template matching to slow
you can try to [train your own classifier](#train-your-own-model)(Note that this process is very long). 


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

https://github.com/DiDawn/AuraBotPOE/assets/95550246/a0d21d3b-bf0f-486b-b3ba-5cfb0f7c8ea2

#### Player POV

Here you can see the bot in action from the player's perspective.
The player is the one in the middle. The bot is the one running around him.

https://github.com/DiDawn/AuraBotPOE/assets/95550246/ae1c77ec-0336-4316-a1e0-682b98386aa3



## Installation
### Environment
If your main account is an aura bot, and you are simply bored of manually following others, you can skip to [the next part](#download-python).

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
You will need to set the following settings in game if you want the bot to work properly:



## Train your own model
