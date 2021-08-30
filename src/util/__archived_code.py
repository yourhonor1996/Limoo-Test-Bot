# --------------------------showing projects based on visibility in bot_main-------------------------- #
        # elif CUR_PROJECT_STATE == PROJECTS_STATES.SHOW_RESULTS:
        #     print(5)
            
        #     # message_split = message.text.split()
        #     # visibility = message_split[1]
        #     # token = message_split[2]
        #     # if not visibility in Consts.Gitlab.VALID_VISIBILITIES:
        #     #     response_text = Commands.Gitlab.TEXT_INVALID_COMMAND
        #     # else:
            
        #     # create a connection to the gilab api- the user_id is stored in the api
        #     connection = await GitlabAsyncConnection.create(session, user.gitlab_tokenen)
            
        #     # if visibility == 'all':
        #     # # get all the private projects using the user id and the given parameters
        #     #     projects = await connection.get_data(f'/users/{connection.user_id}/projects')
        #     # else:
        #     #     projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':visibility})
        #     projects = await connection.get_data(f'/users/{connection.user_id}/projects', parameters={'visibility':'private'})
            
        #     # create response text
        #     response_text = "***Here are your projects:***\n"
        #     filters = Consts.Gitlab.PROJECTS_FIELD_FILTERS
        #     for i, project in enumerate(projects):
        #         response_text += f"**{i+1} - {project['name']}:**\n"
        #         project_text = utility.format_dict_to_text(project, filters)
        #         response_text += project_text
        #     # send the response
        #     CUR_PROJECT_STATE = Commands.Gitlab.STATE_END
        #     await message.reply_in_thread(response_text)