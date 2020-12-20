# FindRoomWithDate Intent

This is to get the neccessary inputs from the user which is retrieved through filling various slots. Slots convert the user utterances into data such as numbers and dates. There are various types of slots:-

* Alexa built-in slots
These are slots are that come in built in with Amazon Alexa. eg. AMAZON.NUMBER, AMAZON.DATE

* Alexa custom slots
These are slots are that are custom defined by the user. For eg. In this skill, a custom 'YES_NO_SLOT' was defined such a way that it accepts the synonyms of 'Yes' and 'No' as inputs and produces boolean output.

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

## Slot details
The following table gives detailed description of various slots used in this particular Intent.

<div class="table-wrap">
	<table class="wrapped confluenceTable tablesorter tablesorter-default stickyTableHeaders" role="grid">
		<colgroup><col><col><col><col></colgroup>
			<thead class="tableFloatingHeader">
				<tr role="row" class="tablesorter-headerRow">
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="0" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Name: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Slot Name</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="1" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Address: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Slot Type</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Input: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Purpose</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Output: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Sample Prompts</p></div></th>
					<th align="center" class="cTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="3" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Output: No sort applied, activate to apply an ascending sort"><div class="tablesorter-header-inner"><p>Sample Utterances</p></div></th>
				</tr>
			</thead>
			<tbody aria-live="polite" aria-relevant="all">
				<tr role="row">
					<td class="cTd"><p>buildingNumber</p></td>
					<td class="cTd"><p>AMAZON.NUMBER</p>
					<td class="cTd"><p>To retrieve the building number for reservation</p>
					<td class="cTd"><p>In which building do you want the room?</p>
					<td class="cTd"><p>{buildingNumber}</p>
									<p>in building {buildingNumber}</p>
									<p>building number {buildingNumber}</p>
									<p>in building number {buildingNumber}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>date</p></td>
					<td class="cTd"><p>AMAZON.DATE</p></td>
					<td class="cTd"><p>To retrieve the date for reservation</p></td>
					<td class="cTd"><p>On which day do you want the room?</p></td>
					<td class="cTd"><p>on {date}</p>
									<p>on {date}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>time</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>duration</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>seats</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>movableSeats</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>projector</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>chalkboard</p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
					<td class="cTd"><p></p></td>
				</tr>				
			</tbody>
		</table>
	</div>

