# RemoveReservation Intent

This intent enables the user to drop the reserved room. It is to be noted that a user is only able to make a single reservation. Therefore this intent cancel the only existing reservation for a user.

There is only a single and mandatory slot **confirmCancellation** for this intent. If the response is a 'Yes' then it drops the only reservation.

Slots convert the user utterances into data such as numbers and dates. There are various types of slots:-

* Alexa built-in slots
These are slots are that come in built in with Amazon Alexa. eg. [**AMAZON.NUMBER**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#number), [**AMAZON.DATE**](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#date)

* Alexa custom slots
These are slots are that are custom defined by the user. eg. **'YES_NO_SLOT'**(explained below).

## Sample utterances
An utterance is a voice command that invokes a particular intent. The intent then prompts the user to fill all the madatory slots. Mandatory slots are those which should be filled compulsarily which are to be converted to data for computation. 

The sample utterances are as below:-
* I want to cancel my reservation
* I would like to cancel my reservation
* I want to drop my reservation 
* I would like to delete my reservation
* I would like to remove my reservation
* I would like to drop my reservation
* I want to remove my reservation
* I want to delete my reservation

### Usage

The below sample gives an idea about the sample requests and responses.

##### Sample Request

```text
Alexa, open lsf room service
	>> ...Hello. Welcome to LSF room service. What can I do for you?
I want to cancel my reservation   
...
```

##### Sample Response

```text
Your reservation has been cancelled....
...
```

## Slot details
The following table gives detailed description of various slots used in this particular Intent.

**Note:** A custom slot **YES_NO_SLOT** has been used in this skill:-
* *Accepts the synonyms of 'Yes' and 'No' as inputs*
* *Produces boolean output*
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
					<td class="cTd"><p>confirmCancellation</p></td>
					<td class="cTd"><p>YES_NO_SLOT</p></td>
					<td class="cTd"><p>Confirmation for cancelling the reservation</p></td>
					<td class="cTd"><p>Do you want to confirm?</p></td>
					<td class="cTd"><p>{confirmCancellation}</p></td>
				</tr>		
			</tbody>
		</table>
	</div>
