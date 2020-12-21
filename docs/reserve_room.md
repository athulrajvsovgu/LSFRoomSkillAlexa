# ReserveRoom Intent

This intent is not meant to function on its own. It is used in conjunction with **[FindRoomWithDate Intent]**(./docs/room_search_date.md) or **[FindRoomImmediately Intent]**(./docs/room_search_immediately.md) using a concept called **[Intent Chaining]**(https://developer.amazon.com/en-US/blogs/alexa/alexa-skills-kit/2019/03/intent-chaining-for-alexa-skill). 

The slots **roomOption**, **roomReserve** for this intent is elicited by prompting the user. Slots convert the user utterances into data such as numbers and dates. There are various types of slots:-

* Alexa built-in slots
These are slots are that come in built in with Amazon Alexa. eg. **[AMAZON.NUMBER]**(https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#number), **[AMAZON.DATE]**(https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#date)

* Alexa custom slots
These are slots are that are custom defined by the user. eg. **'YES_NO_SLOT'**(explained below).

This intent makes use of attributes called **[Session Attributes]**(https://developer.amazon.com/en-US/docs/alexa/custom-skills/manage-skill-session-and-session-attributes.html). It is used to retrieve room search results from the previous session, so that user can specify a choice through 'roomOption' slot After retrieving data from the filled mandatory slot values, it is used to search and find the room details available for reservation, from the LSF Portal. However this is different from the **[FindRoomWithDate Intent]**(./docs/room_search_date.md) that it searches if a room is available from the time of skill invocation.

## Sample utterances
An utterance is a voice command that invokes a particular intent. The intent then prompts the user to fill all the madatory slots. Mandatory slots are those which should be filled compulsarily which are to be converted to data for computation. 

As this intent is used in conjunction with other intents (Intent Chaining) it does not have any sample utterances. Therefore it prompts the user directly to elicit the slot values.

## Slot details
The following table gives detailed description of various slots used in this particular Intent.

**Note:** Two custom slots **YES_NO_SLOT**, **CUSTOM_NUMBER** has been used in this skill:-
* *The YES_NO_SLOT accepts the synonyms of 'Yes' and 'No' as inputs and produces boolean output*
* *The CUSTOM_NUMBER defines a slot that not only accepts numbers but also ordinal format*
* *To get more idea on various slot type please refer the documentation - **[Slot Type Reference]**(https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html)*

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
					<td class="cTd"><p>roomOption</p></td>
					<td class="cTd"><p>CUSTOM_NUMBER</p>
					<td class="cTd"><p>Select an option from the search results</p>
					<td class="cTd"><p>Specify your choice?</p>
					<td class="cTd"><p>option {roomOption}</p>
									<p>{roomOption}</p></td>
				</tr>
				<tr role="row">
					<td class="cTd"><p>roomReserve</p></td>
					<td class="cTd"><p>YES_NO_SLOT</p></td>
					<td class="cTd"><p>Confirmation for the selection</p></td>
					<td class="cTd"><p>Do you want to confirm this choice?</p></td>
					<td class="cTd"><p>{roomReserve}</p></td>
				</tr>		
			</tbody>
		</table>
	</div>


