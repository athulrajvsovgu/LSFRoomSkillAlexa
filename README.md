# Alexa LSF Room Management Skill using ASK Python SDK

This Alexa skill is to manage rooms through the [**LSF Portal**](https://lsf.ovgu.de/qislsf/rds?state=extendedRoomSearch&type=1&next=extendedRoomSearch.vm&nextdir=ressourcenManager&searchCategory=detailedRoomSearch&asi=). The skill prompts the user for necessary inputs and provides appropriate results as can be viewed through the image below. This skill has the following capabilities:-
* Search and reserve a room on specified date and time
* Search and reserve a room immediately
* Cancel reservations
* Welcome back message with reservation details for the user if any exist

The LSF Room Reservation portal looks as below. Options below gives detailed documentation on the various intents.

<img src="https://github.com/athulrajvsovgu/LSFRoomSkillAlexa/blob/dev/img/LSF%20Reservation%20Portal.jpg" />

<table align="center" border="0" cellspacing="0" cellpadding="0" width="100%">
	<tr border="0" cellspacing="0" cellpadding="0">
		<td border="0" cellspacing="0" cellpadding="0"> 
		  <p align="center">
			<img alt="Find room with date" src="./img/1-off._TTH_.png" width="124">
			<br>
			<em>Find room with date</em>
		  </p> 
		</td>
		<td border="0" cellspacing="0" cellpadding="0"> 
		  <p align="center">
			<img alt="Find room immediately" src="./img/2-off._TTH_.png" width="124">
			<br>
			<em>Find room immediately</em>
		  </p> 
		</td>
		<td border="0" cellspacing="0" cellpadding="0"> 
		  <p align="center">
			<img alt="Reserve room" src="./img/3-off._TTH_.png" width="124">
			<br>
			<em>Reserve room</em>
		  </p> 
		</td border="0" cellspacing="0" cellpadding="0">
		<td> 
		  <p align="center">
			<img alt="Cancel reservation" src="./img/4-off._TTH_.png" width="124">
			<br>
			<em>Cancel reservation</em>
		  </p> 
		</td>
		<td border="0" cellspacing="0" cellpadding="0"> 
		  <p align="center">
			<img alt="LSF Portal" src="./img/5-off._TTH_.png" width="124">
			<br>
			<em>LSF Portal</em>
		  </p> 
		</td>
	</tr>
</table>


## Working with the skill

To invoke the skill say ***"open LSF Room Service"***. This launches the skill and looks for various utterances to launch various intents mentioned above.
* For eg. say ***"find a free room in building twenty nine"***. 
* Then it will prompt to collect all the mandatory slot values.
* It retrieves the slot values and uses it to compute the results.
* It also prompts the user to for valid input entry in case of invalid entry. For eg. for a number slot type if a string is entered it prompts the user until a number is entered.
* After computing the results, its converted to voice response and is fed to the user.

**Note:** *A user will only able to make a single reservation.*

### Usage

The below sample gives an idea about the sample requests and responses.

##### Sample Request

```text
Alexa, open lsf room service
	>> ...Hello. Welcome to LSF room service. What can I do for you?
Find a free room in building twenty nine.
	>> ...On which day do you want the room?...
Monday
	>> At what time do you want the room?
Ten o'clock    
	>> ...
...
	>> ...
...
	>> Do you want a chalkboard in your room?
yes    
...
```

##### Sample Response

```text
We have found .... rooms for you....
...
```

## Additional Resources

### Community

* [**Amazon Developer Forums**](https://forums.developer.amazon.com/spaces/165/index.html) - Join the conversation!
* [**Hackster.io**](https://www.hackster.io/amazon-alexa) - See what others are building with Alexa.

### Tutorials & Guides

* [**Voice Design Guide**](https://developer.amazon.com/designing-for-voice/) - A great resource for learning conversational and voice user interface design.
* [**CodeAcademy: Learn Alexa**](https://www.codecademy.com/learn/learn-alexa) - Learn how to build an Alexa Skill from within your browser with this beginner friendly tutorial on CodeAcademy!

### Documentation

*  [**Official Alexa Skills Kit Python SDK**](https://pypi.org/project/ask-sdk/)
*  [**Official Alexa Skills Kit Python SDK Docs**](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
*  [**Official Alexa Skills Kit Documentation**](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)
