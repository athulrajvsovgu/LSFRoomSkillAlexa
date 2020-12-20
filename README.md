# Alexa LSF Room Management Skill using ASK Python SDK

This Alexa skill is to manage rooms through the [LSF Portal](https://lsf.ovgu.de/qislsf/rds?state=extendedRoomSearch&type=1&next=extendedRoomSearch.vm&nextdir=ressourcenManager&searchCategory=detailedRoomSearch&asi=).The skill prompts the user for necessary inputs and provides appropriate results as can be viewed through the image below. This skill has the following capabilities:-
* Search and reserve a room on specified date and time
* Search and reserve a room immediately
* Cancel reservations

The LSF Room Reservation portal looks as below. Options below gives detailed documentation on the various intends.

<img src="https://github.com/athulrajvsovgu/LSFRoomSkillAlexa/blob/dev/img/LSF%20Reservation%20Portal.jpg" />

<table style="border-collapse: collapse; border: none;">
	<tr style="border: none;">
		<td style="border: none;"> 
			<figure>
				<img src="./img/1-off._TTH_.png" width="148">
				<figcaption align="center"><a href="./docs/room_search_date.md">Find room with date</a></figcaption>
			</figure>
		</td>
		<td> 
			<figure>
				<img src="./img/2-off._TTH_.png" width="148">
				<figcaption align="center"><a href="./docs/room_search_immediately.md">Find room immediately</a></figcaption>
			</figure>
		</td>
		<td> 
			<figure>
				<img src="./img/3-off._TTH_.png" width="148">
				<figcaption align="center"><a href="./docs/reserve_room.md">Reserve room</a></figcaption>
			</figure>
		</td>
		<td> 
			<figure>
				<img src="./img/4-off._TTH_.png" width="148">
				<figcaption align="center"><a href="./docs/cancel_reservation.md">Cancel reservation</a></figcaption>
			</figure>
		</td>
		<td> 
			<figure>
				<img src="./img/5-off._TTH_.png" width="148">
				<figcaption align="center"><a href="https://lsf.ovgu.de/qislsf/rds?state=extendedRoomSearch&type=1&next=extendedRoomSearch.vm&nextdir=ressourcenManager&searchCategory=detailedRoomSearch&asi=">LSF Portal</a></figcaption>
			</figure>
		</td>
	</tr>
</table>

## Working

To invoke the skill say "oopen LSF Room Service". This launches the skill and looks for various utterances to launch various intents mentioned above.
* For eg. say "find a free room in building twenty nine". 
* Then it will prompt to collect all the mandatory slot values.
* It retrieves the slot values and uses it to compute the results.
* It also prompts the user to for valid input entry in case of invalid entry. For eg. for a number slot type if a string is entered it prompts the user until a number is entered.
* After computing the results, its converted to voice response and is fed to the user.

### Usage

#### Request

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

#### Response

```text
We have found .... rooms for you....
...
```

## Additional Resources

### Community

* [Amazon Developer Forums](https://forums.developer.amazon.com/spaces/165/index.html) - Join the conversation!
* [Hackster.io](https://www.hackster.io/amazon-alexa) - See what others are building with Alexa.

### Tutorials & Guides

* [Voice Design Guide](https://developer.amazon.com/designing-for-voice/) - A great resource for learning conversational and voice user interface design.
* [CodeAcademy: Learn Alexa](https://www.codecademy.com/learn/learn-alexa) - Learn how to build an Alexa Skill from within your browser with this beginner friendly tutorial on CodeAcademy!

### Documentation

*  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
*  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
*  [Official Alexa Skills Kit Documentation](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)
