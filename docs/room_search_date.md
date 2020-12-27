# FindRoomWithDate Intent

This intent takes neccessary inputs such as building number, date, time etc. from the user which is retrieved through filling various slots. Slots convert the user utterances into data such as numbers and dates. There are various types of slots:-

* Alexa built-in slots
These are slots are that come in built in with Amazon Alexa. eg. [**AMAZON.NUMBER**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#number), [**AMAZON.DATE**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#date)

* Alexa custom slots
These are slots are that are custom defined by the user. eg. **'YES_NO_SLOT'**(explained below).

After retrieving data from the filled mandatory slot values, it is used to search and find the room details available for reservation, from the LSF Portal. However this is different from the [**FindRoomImmediately Intent**](./room_search_immediately.md) that it looks if a room is available on a user specified date and time.

## Sample utterances
An utterance is a voice command that invokes a particular intent. The intent then prompts the user to fill all the madatory slots. Mandatory slots are those which should be filled compulsarily which are to be converted to data for computation. 

The sample utterances are as below:-
* Give me a free room {time}
* find a free room {time}
* find a free room in building {buildingNumber} for  {duration} 
* find a free room for {date}
* find a free room for {date} at {time}  for {duration} 
* Give me a free room in building {buildingNumber}
* find a free room in building {buildingNumber} for {date} at {time}  for {duration}  hours
* Give me a free room in building {buildingNumber} for {date} at {time}  for {duration}  hours

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

## Slot details
The following table gives detailed description of various slots used in this particular Intent.

**Note:** A custom slot ***YES_NO_SLOT*** has been used in this skill:-
* *Accepts the synonyms of 'Yes' and 'No' as inputs produces boolean output*
* *To get more idea on various slot type please refer the documentation - [**Slot Type Reference**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html)*

<div class="table-wrap">
	<table class="wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders" role="grid">
		<colgroup><col><col><col><col></colgroup>
			<thead class="tableFloatingHeader">
				<tr role="row" class="tablesorter-headerRow">
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Name: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Slot Name</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Address: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Slot Type</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Input: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Description</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Output: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Sample Prompts</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Output: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Sample Utterances</p></div></th>
				</tr>
			</thead>
			<tbody aria-live="polite" aria-relevant="all">
				<tr role="row">
					<td class="cTd"><p>buildingNumber</p></td>
					<td class="cTd"><p>AMAZON.NUMBER</p>
					<td class="cTd"><p>The building number for reservation</p>
					<td class="cTd"><p>In which building do you want the room?</p>
					<td class="cTd"><p>* {buildingNumber}</p>
									<p>* in building {buildingNumber}</p>
									<p>* building number {buildingNumber}</p>
									<p>* in building number {buildingNumber}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>date</p></td>
					<td class="cTd"><p>AMAZON.DATE</p></td>
					<td class="cTd"><p>The date for reservation</p></td>
					<td class="cTd"><p>On which day do you want the room?</p></td>
					<td class="cTd"><p>* {date}</p>
									<p>* on {date}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>time</p></td>
					<td class="cTd"><p>AMAZON.TIME</p></td>
					<td class="cTd"><p>The time for reservation</p></td>
					<td class="cTd"><p>At what time do you want the room?</p></td>
					<td class="cTd"><p>* I want the room {time}</p>
                                    <p>* {time}</p>
									<p>* I want the room at {time}</p>
                                    <p>* at {time}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>duration</p></td>
					<td class="cTd"><p>AMAZON.NUMBER</p></td>
					<td class="cTd"><p>The duration for reservation</p></td>
					<td class="cTd"><p>For how many hours do you want the room?</p></td>
					<td class="cTd"><p>* I want the room for {duration} hours</p>
                                    <p>* {duration} hours</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>seats</p></td>
					<td class="cTd"><p>AMAZON.NUMBER</p></td>
					<td class="cTd"><p>The seats required in the room</p></td>
					<td class="cTd"><p>How many seats do you want in the room?</p></td>
					<td class="cTd"><p>* I want {seats} seats</p>
                                    <p>* {seats}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>movableSeats</p></td>
					<td class="cTd"><p>YES_NO_SLOT</p></td>
					<td class="cTd"><p>Check if the user needs fixed or movable seats</p></td>
					<td class="cTd"><p>Do you want movables seats?</p></td>
					<td class="cTd"><p>{movableSeats}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>projector</p></td>
					<td class="cTd"><p>YES_NO_SLOT</p></td>
					<td class="cTd"><p>Check if the user needs an lcd projector</p></td>
					<td class="cTd"><p>Do you want an LCD projector in the room?</p></td>
					<td class="cTd"><p>{projector}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>chalkboard</p></td>
					<td class="cTd"><p>YES_NO_SLOT</p></td>
					<td class="cTd">Check if the user needs an chalkboard<p></p></td>
					<td class="cTd">Do you want a chalk board in the room?<p></p></td>
					<td class="cTd"><p>{chalkboard}</p></td>
				</tr>				
			</tbody>
		</table>
	</div>

