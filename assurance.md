# Iteration2 – Assurance

## Verification & Validation
**Verification**
We used Pytest in Iteration 1 to test the functionalities of the backend functions. And Python converges report allowed us to view how much the tests covered in the backend functions. In addition, advanced rest client was used as a temporary tool to test the functions in the server and we also connected the backend functions to the frontend provided by the lecturer. It indicates that most of the functions were working with advanced rest client, but did not work in frontend because some of the setups were different. Moreover, some functions were unable to test on the current stage, like standup. Furthermore, Pylint was a great tool to help us adjust the appropriate style for Python coding.

**Validation**
Producing the acceptance criteria from user stories is an effective way to see whether it meets the client's requirements. We can check whether we have achieved all the features by breaking down each user story into several requirements with details, including scenarios, display detail and functionalities, where normally the scenarios indicate the relevant functions, the display detail indicates how frontend designed the website and functionalities demonstrate the features that the website should contain. On the current stage, we mainly focus on checking features with the functionalities of the backend functions, therefore, the backend should meet the client’s requirements.

## Acceptance Criteria
### auth/login
Scenario: login the slackr through calling auth/login.
* A user could log in when he entered the correct email and password.
* A user could log in when he registered before.
* Link to the channel page when user login successful.
* Display **Value error message** if the email entered is not a valid email when user login.
* Display **Value error message** if the user entered an email that does not belong to him.
* Display **Value error message** if the user entered the password that not correct.

### auth/logout
Scenario: logout the slackr through calling auth/logout.
* A user could log out when he logged in before.

### auth/register
Scenario: register the slackr through calling auth/register.
* A user could register when he does not register before.
* A user could register when he entered the correct email address, name and password.
* Link to the login page when the user registered successfully.
* Display **Value error message** if the email address that the user entered is already being used.
* Display **Value error message** if the first name that the user entered is not between 1 and 50 characters in length.
* Display **Value error message** if the last name that the user entered is not between 1 and 50 characters in length.
* Display **Value error message** if the user entered the password that less than 6 characters long.

### auth/passwordreset/request
Scenario: Receiving the reset password email through calling auth/register.
* A user could reset the password when he forgot the password.
* A user could reset the password when he registered before.
* A user could use the secret code when he is the one who sent  this email.
* A user could receive an email containing the secret code when he reset the password.

### auth/passwordreset/reset
Scenario: Resetting the password through calling auth/register.
* A user could reset the password when he forgot the password.
* A user could reset the password by using the correct secret code.
* Display **Value error message** if the reset code entered is invalid.
* Display **Value error message** if the password entered is invalid.

### channel/invite
Scenario: Invites a user to join a channel through calling channel/invite
* A user could be invited to join the channel.
* A user could join the channel immediately when he are invited.
* Display **Value error message** if the channel id is not invalid.
* Display **Value error message** if the invited user is not invalid.
* Display **Access error message** if the authorised user is not a member of the channel.



### channel/details
Scenario: Providing basic details about the channel through calling channel/details
* A user could view the details of channel when he joined in this channel before.
* Display **Value error message** if the channel id is not invalid.
* Display **Access error message** if the authorised user is not a member of the channel.

### channel/messages
Scenario: Invites a user to join a channel through calling channel/invite
* A user could be invited to join the channel.
* A user could join the channel immediately when he are invited.
* Display **Value error message** if the channel id is not invalid.
* Display **Value error message** if the start is greater than the total number of messages in the channel.
* Display **Access error message** if the authorised user is not a member of the channel.

### channel/leave
Scenario: Leaving the channel through calling channel/leave.
* A member could leave the channel that he has joined before.
* A member could not leave the channel that he has not joined before.
* Display **Value error message** if the member wants to leave an invalid channel.

### channel/join
Scenario: Joining the channel through calling channel/join.
* A member could join the public channel without permission.
* An owner or admin of slackr could join the private channel.
* A user becomes a member when he join the channel.
* Display **Value error message** if a member wants to join an invalid channel.
* Display **Access error message** if the member of slackr wants to join the private channel.

### channel/addowner
Scenario: Make user with user id an owner of this channel through calling channel/addowner.
* A member could be added as an owner of channel by the authorised user.
* An owner cannot be added as an owner of the channel.
* Display **Value error message** if a member wants to join an invalid channel.
* Display **Access error message** if the authorised user is not an owner of the channel.
* Display **Access error message** if the authorised user is not an owner of the slackr.

### channel/removeowner
Scenario: Remove user with user id an owner of this channel through calling channel/removeowner.
* An owner could be removed as an owner of channel by the authorised user.
* A member cannot be removed as an owner of the channel.
* Display **Value error message** if a member wants to join an invalid channel.
* Display **Access error message** if the authorised user is not an owner of the channel.
* Display **Access error message** if the authorised user is not an owner of the slackr.

### channel/list
Scenario: Provide a list of all channels that the authorised user is part of through calling channel/list.
* A user could view the list and the details of the list that he has joined before. 

### channel/listall
Scenario: Provide a list of all channels that the authorised user is part of through calling channel/list.
* A user could view the whole channel list and their details.

### channel/create
Scenario: Creates a new channel through calling channel/create.
* A user can choose public or private when he creates the channel.
* A user who creates the channel will become the owner of the channel.
* A user could set the name of the channel when he created the channel.
* Link to the channel page if create is successful.
* Display **Value error message** if the length of the channel name is more than 20 characters long.

### message/sendlater
Scenario: Sending a message at a specified time in the future through calling message/sendlater.
* A user who has joined the channel could send a message at a specified time on this channel.
* Display **Value error message** if the specified time that member set is not in the future.
* Display **Value error message** if a member wants to send a message more than 1000 characters.
* Display **Value error message** if a member wants to join an invalid channel.
* Display **Access error message** if the authorised user has not joined the channel they are trying to post to.

### message/sendlater
* Scenario: Sending a message through calling message/send.
* A user who has joined the channel could send a message on this channel.
* Display **Value error message** if a member wants to send a message more than 1000 characters.
* Display **Value error message** if a member wants to join an invalid channel.
* Display **Access error message** if the authorised user has not joined the channel they are trying to post to.

### message/remove
Scenario: Removing a message through calling message/remove by referring token and message_id.
* Any member can remove his own message that he sent before.
* An owner of a channel can remove any message on the channel.
* An owner/admin of the Slackr is able to remove any message in any channel.
* Display **Value error message** if the message id does not exist / not valid.
* Display **Access error message** if a member of channel tries to remove messages that are sent by others.

### message/edit
Scenario: Edit a message in the channel through calling message/remove by referring token, message_id and the edited message.
* Any member is able to edit his own message that he sent before.
* An owner/admin of the Slackr can edit any message in any channel.
* Display **Access error message** if a member of channel tries to remove messages that are sent by others.

### message/react 
Scenario: Select a message and react a ‘thumbs up’ emoji to the dialogue box by calling message/react through referring token, message_id and the react_id.
* Any member is able to react to any message on the channel that this he joined.
* Display **Value error message** if the authorised user that called this function has not joined the channel that the message is in.
* Display **Value error message** if the react id is not valid(if the react id is not 1).
* Display **Value error message** if the message already has a react.

### message/unreact
Scenario: Remove react in a specific message by calling message/unreact through referring token, message_id and the react_id.
* Any member is able to unreact to any message in the channel that this he joined.
* Display **Value error message** if the authorised user that called this function has not joined the channel that the message is in.
* Display **Value error message** if the react id that the user is not valid(if the react id is not 1).
* Display **Value error message** if the message does not have a react with react_id.

### message/pin
Scenario: Pin in a specific message by calling message/unreact, which is highlighted and pinned to the beginning of the message through referring token and message_id.
* An owner/admin of the Slackr can pin any message in the channel.
* Display **Value error message** if the message with message_id does not exist / not valid.
* Display **Value error message** if the authorised user is not an owner or admin of the slackr.
* Display **Value error message** if the message is already been pinned.
* Display **Access error message** if the authorised user that called this function has not joined the channel that the message is in.

### message/unpin
Scenario: Unpin in a specific message by calling message/unreact, which is highlighted and pinned to the beginning of the message through referring token and message_id.
* An owner/admin of the Slackr can pin any message in the channel.
* Display **Value error message** if the message with message_id does not exist / not valid.
* Display **Value error message** if the authorised user is not an owner or admin of the slackr.
* Display **Value error message** if the message has not been pinned.
* Display **Access error message** if the authorised user that called this function has not joined the channel that the message is in.

### User_profile
Scenario: A user can look at basic information (including email, first name, last name, and handle) though calling user_profile by referring token and user_id.
* All members can look at any member’s profile.
* Display **Value error message** if the user does not exist (the u_id or token is not valid).


### User_profile_setname
Scenario: Update first and/or last name.
* Display **Value error message** if first or last name is more than 50 characters in length.

### User_profile_setemail
Scenario: Update email address.
* Email can be updated even though new email and previous email are the same.
* Display **Value error message** if the email address is not valid.
* Display **Value error message** if the email address is already used by another user.

### User_profile_sethandle
Scenario: Update authorised user’s handle.
* Handle is a display name .
* Display **Value error message** if handle is either less than 3 characters or more than 20 characters in length.
* Display **Value error message** if the handle is already used by another user.

### Standup_start
Scenario: Sends a message and calls ‘standup_start’ function.
* Buffered during 15 minute window.
* At the end of 15 minute window a message will be added to the message queue in the channel.
* Display **Value error message** if channel ID is not a valid channel.
* Display **Value error message** if an active standup is currently running in this channel.
* Display **Access error message** if the authorised user is not a member of the channel that the message is within.

### Standup_send
Scenario: Sends a message to get buffered in the standup queue.
* Display **Value error message** if channel ID is not a valid channel.
* Display **Value error message** if message is more than 1000 characters.
* Display **Value error message** if an active standup is not currently running in this channel.
* Display **Access error message** if the authorised user is not a member of the channel that the message is within.

### Search
Scenario: Search with a query.
* Given a query string, return a collection of messages in all of the channels that the user has joined that match the query.

### Admin_userpermission_change
Scenario: Admin or owner gets permission with user ID. 
* Given a User by their user ID, set their permissions to new permissions described by permission_id.
* Display **Value error message** if u_id does not refer to a valid user.
* Display **Value error message** if permission_id does not refer to a value permission.
* Display **Access error message** if the authorised user is not an admin or owner.


