"""Generated from spec/openapi.yaml by tools/generate.py. Do not edit.

One method per Figma REST API operation, for both the sync and async clients.
`_call` is implemented by figmapy.client.
"""

# fmt: off
# flake8: noqa

from __future__ import annotations

from typing import Any, Optional, Union

from . import models

FIGMA_SPEC_VERSION = "0.42.0"



class SyncEndpoints:

    def delete_comment(
        self,
        file_key: str,
        comment_id: str,
    ) -> Union["models.DeleteCommentResponse", dict]:
        """Delete a comment

        Deletes a specific comment. Only the person who made the comment is allowed to delete it.

        DELETE /v1/files/{file_key}/comments/{comment_id}
        """
        return self._call(
            'DELETE',
            '/v1/files/{file_key}/comments/{comment_id}'.format(file_key=file_key, comment_id=comment_id),
            params=None,
            json_body=None,
            model=models.DeleteCommentResponse,
        )


    def delete_comment_reaction(
        self,
        file_key: str,
        comment_id: str,
        *,
        emoji: str,
    ) -> Union["models.DeleteCommentReactionResponse", dict]:
        """Delete a reaction

        Deletes a specific comment reaction. Only the person who made the reaction is allowed to delete it.

        DELETE /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return self._call(
            'DELETE',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params={'emoji': emoji},
            json_body=None,
            model=models.DeleteCommentReactionResponse,
        )


    def delete_dev_resource(
        self,
        file_key: str,
        dev_resource_id: str,
    ) -> Union[Any, dict]:
        """Delete dev resource

        Delete a dev resource from a file

        DELETE /v1/files/{file_key}/dev_resources/{dev_resource_id}
        """
        return self._call(
            'DELETE',
            '/v1/files/{file_key}/dev_resources/{dev_resource_id}'.format(file_key=file_key, dev_resource_id=dev_resource_id),
            params=None,
            json_body=None,
            model=None,
        )


    def delete_webhook(
        self,
        webhook_id: str,
    ) -> Union["models.WebhookV2", dict]:
        """Delete a webhook

        Deletes the specified webhook. This operation cannot be reversed.

        DELETE /v2/webhooks/{webhook_id}
        """
        return self._call(
            'DELETE',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.WebhookV2,
        )


    def get_activity_logs(
        self,
        *,
        events: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: Optional[float] = None,
        order: Optional[str] = None,
    ) -> Union["models.GetActivityLogsResponse", dict]:
        """Get activity logs

        Returns a list of activity log events

        GET /v1/activity_logs
        """
        return self._call(
            'GET',
            '/v1/activity_logs',
            params={'events': events, 'start_time': start_time, 'end_time': end_time, 'limit': limit, 'order': order},
            json_body=None,
            model=models.GetActivityLogsResponse,
        )


    def get_ai_usage_daily(
        self,
        *,
        start_date: str,
        end_date: str,
        user_email: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.GetAiUsageDailyResponse", dict]:
        """Get daily AI credit usage

        Returns per-user, per-day AI credit usage for the plan associated with the calling token. This endpoint requires a plan access token with the `org:ai_metering_usage_read` scope.

        GET /v1/ai_usage/daily
        """
        return self._call(
            'GET',
            '/v1/ai_usage/daily',
            params={'start_date': start_date, 'end_date': end_date, 'user_email': user_email, 'limit': limit, 'cursor': cursor},
            json_body=None,
            model=models.GetAiUsageDailyResponse,
        )


    def get_comment_reactions(
        self,
        file_key: str,
        comment_id: str,
        *,
        cursor: Optional[str] = None,
    ) -> Union["models.GetCommentReactionsResponse", dict]:
        """Get reactions for a comment

        Gets a paginated list of reactions left on the comment.

        GET /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params={'cursor': cursor},
            json_body=None,
            model=models.GetCommentReactionsResponse,
        )


    def get_comments(
        self,
        file_key: str,
        *,
        as_md: Optional[bool] = None,
    ) -> Union["models.GetCommentsResponse", dict]:
        """Get comments in a file

        Gets a list of comments left on the file.

        GET /v1/files/{file_key}/comments
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/comments'.format(file_key=file_key),
            params={'as_md': as_md},
            json_body=None,
            model=models.GetCommentsResponse,
        )


    def get_component(
        self,
        key: str,
    ) -> Union["models.GetComponentResponse", dict]:
        """Get component

        Get metadata on a component by key.

        GET /v1/components/{key}
        """
        return self._call(
            'GET',
            '/v1/components/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetComponentResponse,
        )


    def get_component_set(
        self,
        key: str,
    ) -> Union["models.GetComponentSetResponse", dict]:
        """Get component set

        Get metadata on a published component set by key.

        GET /v1/component_sets/{key}
        """
        return self._call(
            'GET',
            '/v1/component_sets/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetComponentSetResponse,
        )


    def get_dev_resources(
        self,
        file_key: str,
        *,
        node_ids: Optional[str] = None,
    ) -> Union["models.GetDevResourcesResponse", dict]:
        """Get dev resources

        Get dev resources in a file

        GET /v1/files/{file_key}/dev_resources
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/dev_resources'.format(file_key=file_key),
            params={'node_ids': node_ids},
            json_body=None,
            model=models.GetDevResourcesResponse,
        )


    def get_developer_logs(
        self,
        *,
        token_type: Optional[str] = None,
        token: Optional[str] = None,
        token_name: Optional[str] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        event_source: Optional[str] = None,
        date_range: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.PostDeveloperLogsResponse", dict]:
        """Get developer logs

        Returns a list of developer log entries for REST API and MCP server requests made within the organization. This endpoint requires a plan access token with the `org:developer_log_read` scope.

        POST /v1/developer_logs
        """
        return self._call(
            'POST',
            '/v1/developer_logs',
            params=None,
            json_body={'token_type': token_type, 'token': token, 'token_name': token_name, 'user_email': user_email, 'ip_address': ip_address, 'event_source': event_source, 'date_range': date_range, 'limit': limit, 'cursor': cursor},
            model=models.PostDeveloperLogsResponse,
        )


    def get_file(
        self,
        file_key: str,
        *,
        version: Optional[str] = None,
        ids: Optional[str] = None,
        depth: Optional[float] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetFileResponse", dict]:
        """Get file JSON

        Returns the document identified by `file_key` as a JSON object. The file key can be parsed from any Figma file url: `https://www.figma.com/file/{file_key}/{title}`.

        The `document` property contains a node of type `DOCUMENT`.

        The `components` property contains a mapping from node IDs to component metadata. This is to help you determine which components each instance comes from.

        GET /v1/files/{file_key}
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}'.format(file_key=file_key),
            params={'version': version, 'ids': ids, 'depth': depth, 'geometry': geometry, 'plugin_data': plugin_data, 'branch_data': branch_data},
            json_body=None,
            model=models.GetFileResponse,
        )


    def get_file_component_sets(
        self,
        file_key: str,
    ) -> Union["models.GetFileComponentSetsResponse", dict]:
        """Get file component sets

        Get a list of published component sets within a file library.

        GET /v1/files/{file_key}/component_sets
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/component_sets'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileComponentSetsResponse,
        )


    def get_file_components(
        self,
        file_key: str,
    ) -> Union["models.GetFileComponentsResponse", dict]:
        """Get file components

        Get a list of published components within a file library.

        GET /v1/files/{file_key}/components
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/components'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileComponentsResponse,
        )


    def get_file_meta(
        self,
        file_key: str,
    ) -> Union["models.GetFileMetaResponse", dict]:
        """Get file metadata

        Get file metadata

        GET /v1/files/{file_key}/meta
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/meta'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileMetaResponse,
        )


    def get_file_nodes(
        self,
        file_key: str,
        *,
        ids: str,
        version: Optional[str] = None,
        depth: Optional[float] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None,
    ) -> Union["models.GetFileNodesResponse", dict]:
        """Get file JSON for specific nodes

        Returns the nodes referenced to by `ids` as a JSON object. The nodes are retrieved from the Figma file referenced to by `file_key`.

        The node ID and file key can be parsed from any Figma node url: `https://www.figma.com/file/{file_key}/{title}?node-id={id}`

        The `name`, `lastModified`, `thumbnailUrl`, `editorType`, and `version` attributes are all metadata of the specified file.

        ...

        GET /v1/files/{file_key}/nodes
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/nodes'.format(file_key=file_key),
            params={'ids': ids, 'version': version, 'depth': depth, 'geometry': geometry, 'plugin_data': plugin_data},
            json_body=None,
            model=models.GetFileNodesResponse,
        )


    def get_file_styles(
        self,
        file_key: str,
    ) -> Union["models.GetFileStylesResponse", dict]:
        """Get file styles

        Get a list of published styles within a file library.

        GET /v1/files/{file_key}/styles
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/styles'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileStylesResponse,
        )


    def get_file_versions(
        self,
        file_key: str,
        *,
        page_size: Optional[float] = None,
        before: Optional[float] = None,
        after: Optional[float] = None,
    ) -> Union["models.GetFileVersionsResponse", dict]:
        """Get versions of a file

        This endpoint fetches the version history of a file, allowing you to see the progression of a file over time. You can then use this information to render a specific version of the file, via another endpoint.

        GET /v1/files/{file_key}/versions
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/versions'.format(file_key=file_key),
            params={'page_size': page_size, 'before': before, 'after': after},
            json_body=None,
            model=models.GetFileVersionsResponse,
        )


    def get_folder_files(
        self,
        folder_id: str,
        *,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetFolderFilesResponse", dict]:
        """Get files in a folder

        Get a list of the files directly within the specified folder.

        GET /v2/folders/{folder_id}/files
        """
        return self._call(
            'GET',
            '/v2/folders/{folder_id}/files'.format(folder_id=folder_id),
            params={'branch_data': branch_data},
            json_body=None,
            model=models.GetFolderFilesResponse,
        )


    def get_folder_folders(
        self,
        folder_id: str,
    ) -> Union["models.GetFolderFoldersResponse", dict]:
        """Get subfolders in a folder

        Get a list of the direct subfolders within the specified folder.

        GET /v2/folders/{folder_id}/folders
        """
        return self._call(
            'GET',
            '/v2/folders/{folder_id}/folders'.format(folder_id=folder_id),
            params=None,
            json_body=None,
            model=models.GetFolderFoldersResponse,
        )


    def get_folder_meta(
        self,
        folder_id: str,
    ) -> Union["models.GetFolderMetaResponse", dict]:
        """Get folder metadata

        Get metadata for a folder (name, thumbnail, file count, timestamps) without enumerating its files.

        GET /v2/folders/{folder_id}/meta
        """
        return self._call(
            'GET',
            '/v2/folders/{folder_id}/meta'.format(folder_id=folder_id),
            params=None,
            json_body=None,
            model=models.GetFolderMetaResponse,
        )


    def get_image_fills(
        self,
        file_key: str,
    ) -> Union["models.GetImageFillsResponse", dict]:
        """Get image fills

        Returns download links for all images present in image fills in a document. Image fills are how Figma represents any user supplied images. When you drag an image into Figma, we create a rectangle with a single fill that represents the image, and the user is able to transform the rectangle (and properties on the fill) as they wish.

        This endpoint returns a mapping from image references to the URLs at which the images may be download. Image URLs will expire after no more than 14 days. Image references are located in the output of the GET files endpoint under the `imageRef` attribute in a `Paint`.

        GET /v1/files/{file_key}/images
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/images'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetImageFillsResponse,
        )


    def get_images(
        self,
        file_key: str,
        *,
        ids: str,
        version: Optional[str] = None,
        scale: Optional[float] = None,
        format: Optional[str] = None,
        svg_outline_text: Optional[bool] = None,
        svg_include_id: Optional[bool] = None,
        svg_include_node_id: Optional[bool] = None,
        svg_simplify_stroke: Optional[bool] = None,
        contents_only: Optional[bool] = None,
        use_absolute_bounds: Optional[bool] = None,
    ) -> Union["models.GetImagesResponse", dict]:
        """Render images of file nodes

        Renders images from a file.

        If no error occurs, `"images"` will be populated with a map from node IDs to URLs of the rendered images, and `"status"` will be omitted. The image assets will expire after 30 days. Images up to 32 megapixels can be exported. Any images that are larger will be scaled down.

        Important: the image map may contain values that are `null`. This indicates that rendering of that specific node has failed. This may be due to the node id not existing, or other reasons such has the node having no renderable components. It is guaranteed that any node that was requested for rendering will be represented in this map whether or not the render succeeded.

        ...

        GET /v1/images/{file_key}
        """
        return self._call(
            'GET',
            '/v1/images/{file_key}'.format(file_key=file_key),
            params={'ids': ids, 'version': version, 'scale': scale, 'format': format, 'svg_outline_text': svg_outline_text, 'svg_include_id': svg_include_id, 'svg_include_node_id': svg_include_node_id, 'svg_simplify_stroke': svg_simplify_stroke, 'contents_only': contents_only, 'use_absolute_bounds': use_absolute_bounds},
            json_body=None,
            model=models.GetImagesResponse,
        )


    def get_library_analytics_component_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsComponentActionsResponse", dict]:
        """Get library analytics component action data.

        Returns a list of library analytics component actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/component/actions
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/component/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsComponentActionsResponse,
        )


    def get_library_analytics_component_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsComponentUsagesResponse", dict]:
        """Get library analytics component usage data.

        Returns a list of library analytics component usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/component/usages
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/component/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsComponentUsagesResponse,
        )


    def get_library_analytics_style_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsStyleActionsResponse", dict]:
        """Get library analytics style action data.

        Returns a list of library analytics style actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/style/actions
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/style/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsStyleActionsResponse,
        )


    def get_library_analytics_style_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsStyleUsagesResponse", dict]:
        """Get library analytics style usage data.

        Returns a list of library analytics style usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/style/usages
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/style/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsStyleUsagesResponse,
        )


    def get_library_analytics_variable_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsVariableActionsResponse", dict]:
        """Get library analytics variable action data.

        Returns a list of library analytics variable actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/variable/actions
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/variable/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsVariableActionsResponse,
        )


    def get_library_analytics_variable_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsVariableUsagesResponse", dict]:
        """Get library analytics variable usage data.

        Returns a list of library analytics variable usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/variable/usages
        """
        return self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/variable/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsVariableUsagesResponse,
        )


    def get_local_variables(
        self,
        file_key: str,
    ) -> Union["models.GetLocalVariablesResponse", dict]:
        """Get local variables

        **This API is available to full members of Enterprise orgs.**

        The `GET /v1/files/:file_key/variables/local` endpoint lets you enumerate local variables created in the file and remote variables used in the file. Remote variables are referenced by their `subscribed_id`.

        As a part of the Variables related API additions, the `GET /v1/files/:file_key` endpoint now returns a `boundVariables` property, containing the `variableId` of the bound variable. The `GET /v1/files/:file_key/variables/local` endpoint can be used to get the full variable or variable collection object.

        ...

        GET /v1/files/{file_key}/variables/local
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/variables/local'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetLocalVariablesResponse,
        )


    def get_me(
        self,
    ) -> Union["models.GetMeResponse", dict]:
        """Get current user

        Returns the user information for the currently authenticated user.

        GET /v1/me
        """
        return self._call(
            'GET',
            '/v1/me',
            params=None,
            json_body=None,
            model=models.GetMeResponse,
        )


    def get_o_embed(
        self,
        *,
        url: str,
        maxwidth: Optional[int] = None,
        maxheight: Optional[int] = None,
    ) -> Union["models.GetOEmbedResponse", dict]:
        """Get oEmbed data

        Returns oEmbed data for a Figma file or published Make site URL, following the [oEmbed specification](https://oembed.com/).

        GET /v1/oembed
        """
        return self._call(
            'GET',
            '/v1/oembed',
            params={'url': url, 'maxwidth': maxwidth, 'maxheight': maxheight},
            json_body=None,
            model=models.GetOEmbedResponse,
        )


    def get_payments(
        self,
        *,
        plugin_payment_token: Optional[str] = None,
        user_id: Optional[str] = None,
        community_file_id: Optional[str] = None,
        plugin_id: Optional[str] = None,
        widget_id: Optional[str] = None,
    ) -> Union["models.GetPaymentsResponse", dict]:
        """Get payments

        There are two methods to query for a user's payment information on a plugin, widget, or Community file. The first method, using plugin payment tokens, is typically used when making queries from a plugin's or widget's code. The second method, providing a user ID and resource ID, is typically used when making queries from anywhere else.

        Note that you can only query for resources that you own. In most cases, this means that you can only query resources that you originally created.

        GET /v1/payments
        """
        return self._call(
            'GET',
            '/v1/payments',
            params={'plugin_payment_token': plugin_payment_token, 'user_id': user_id, 'community_file_id': community_file_id, 'plugin_id': plugin_id, 'widget_id': widget_id},
            json_body=None,
            model=models.GetPaymentsResponse,
        )


    def get_project_files(
        self,
        project_id: str,
        *,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetProjectFilesResponse", dict]:
        """[Deprecated] Get files in a project

        Deprecated in favor of [Get files in a folder](https://developers.figma.com/docs/rest-api/folders-endpoints/). Get a list of all the Files within the specified project (now called a "folder").

        GET /v1/projects/{project_id}/files
        """
        return self._call(
            'GET',
            '/v1/projects/{project_id}/files'.format(project_id=project_id),
            params={'branch_data': branch_data},
            json_body=None,
            model=models.GetProjectFilesResponse,
        )


    def get_project_meta(
        self,
        project_id: str,
    ) -> Union["models.GetProjectMetaResponse", dict]:
        """[Deprecated] Get project metadata

        Deprecated in favor of [Get folder metadata](https://developers.figma.com/docs/rest-api/folders-endpoints/). Get metadata for a project (now called a "folder").

        GET /v1/projects/{project_id}/meta
        """
        return self._call(
            'GET',
            '/v1/projects/{project_id}/meta'.format(project_id=project_id),
            params=None,
            json_body=None,
            model=models.GetProjectMetaResponse,
        )


    def get_published_variables(
        self,
        file_key: str,
    ) -> Union["models.GetPublishedVariablesResponse", dict]:
        """Get published variables

        **This API is available to full members of Enterprise orgs.**

        The `GET /v1/files/:file_key/variables/published` endpoint returns the variables that are published from the given file.

        The response for this endpoint contains some key differences compared to the `GET /v1/files/:file_key/variables/local` endpoint:

        - Each variable and variable collection contains a `subscribed_id`.
        - Modes are omitted for published variable collections

        ...

        GET /v1/files/{file_key}/variables/published
        """
        return self._call(
            'GET',
            '/v1/files/{file_key}/variables/published'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetPublishedVariablesResponse,
        )


    def get_style(
        self,
        key: str,
    ) -> Union["models.GetStyleResponse", dict]:
        """Get style

        Get metadata on a style by key.

        GET /v1/styles/{key}
        """
        return self._call(
            'GET',
            '/v1/styles/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetStyleResponse,
        )


    def get_team_component_sets(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamComponentSetsResponse", dict]:
        """Get team component sets

        Get a paginated list of published component sets within a team library.

        GET /v1/teams/{team_id}/component_sets
        """
        return self._call(
            'GET',
            '/v1/teams/{team_id}/component_sets'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamComponentSetsResponse,
        )


    def get_team_components(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamComponentsResponse", dict]:
        """Get team components

        Get a paginated list of published components within a team library.

        GET /v1/teams/{team_id}/components
        """
        return self._call(
            'GET',
            '/v1/teams/{team_id}/components'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamComponentsResponse,
        )


    def get_team_folders(
        self,
        team_id: str,
    ) -> Union["models.GetTeamFoldersResponse", dict]:
        """Get top-level folders in a team

        Get a list of the top-level folders (previously called "projects") within the specified team. Subfolders can be traversed with the GET /v2/folders/{folder_id}/folders endpoint. It is not possible to programmatically obtain team IDs. To obtain a team ID, navigate to the team page in the Figma file browser. The team ID is present in the URL after the word team. For example, in `https://www.figma.com/files/181033233908053158/team/1535685101263221741`, the team ID is `1535685101263221741`.

        GET /v2/teams/{team_id}/folders
        """
        return self._call(
            'GET',
            '/v2/teams/{team_id}/folders'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamFoldersResponse,
        )


    def get_team_projects(
        self,
        team_id: str,
    ) -> Union["models.GetTeamProjectsResponse", dict]:
        """[Deprecated] Get projects in a team

        Deprecated in favor of [Get top-level folders in a team](https://developers.figma.com/docs/rest-api/folders-endpoints/). You can use this endpoint to get a list of the top-level Projects (now called "folders") within the specified team. This will only return projects visible to the authenticated user or owner of the developer token. Note: it is not currently possible to programmatically obtain the team id of a user just from a token. To obtain a team id, navigate to a team page of a team you are a part of. The team id will be present in the URL after the word team and before your team name.

        GET /v1/teams/{team_id}/projects
        """
        return self._call(
            'GET',
            '/v1/teams/{team_id}/projects'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamProjectsResponse,
        )


    def get_team_styles(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamStylesResponse", dict]:
        """Get team styles

        Get a paginated list of published styles within a team library.

        GET /v1/teams/{team_id}/styles
        """
        return self._call(
            'GET',
            '/v1/teams/{team_id}/styles'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamStylesResponse,
        )


    def get_team_webhooks(
        self,
        team_id: str,
    ) -> Union["models.GetTeamWebhooksResponse", dict]:
        """[Deprecated] Get team webhooks

        Returns all webhooks registered under the specified team.

        GET /v2/teams/{team_id}/webhooks
        """
        return self._call(
            'GET',
            '/v2/teams/{team_id}/webhooks'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamWebhooksResponse,
        )


    def get_webhook(
        self,
        webhook_id: str,
    ) -> Union["models.WebhookV2", dict]:
        """Get a webhook

        Get a webhook by ID.

        GET /v2/webhooks/{webhook_id}
        """
        return self._call(
            'GET',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.WebhookV2,
        )


    def get_webhook_requests(
        self,
        webhook_id: str,
    ) -> Union["models.GetWebhookRequestsResponse", dict]:
        """Get webhook requests

        Returns all webhook requests sent within the last week. Useful for debugging.

        GET /v2/webhooks/{webhook_id}/requests
        """
        return self._call(
            'GET',
            '/v2/webhooks/{webhook_id}/requests'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.GetWebhookRequestsResponse,
        )


    def get_webhooks(
        self,
        *,
        context: Optional[str] = None,
        context_id: Optional[str] = None,
        plan_api_id: Optional[str] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.GetWebhooksResponse", dict]:
        """Get webhooks by context or plan

        Returns a list of webhooks corresponding to the context or plan provided, if they exist. For plan, the webhooks for all contexts that you have access to will be returned, and theresponse is paginated

        GET /v2/webhooks
        """
        return self._call(
            'GET',
            '/v2/webhooks',
            params={'context': context, 'context_id': context_id, 'plan_api_id': plan_api_id, 'cursor': cursor},
            json_body=None,
            model=models.GetWebhooksResponse,
        )


    def post_comment(
        self,
        file_key: str,
        *,
        message: str,
        comment_id: Optional[str] = None,
        client_meta: Optional[Any] = None,
    ) -> Union["models.Comment", dict]:
        """Add a comment to a file

        Posts a new comment on the file.

        POST /v1/files/{file_key}/comments
        """
        return self._call(
            'POST',
            '/v1/files/{file_key}/comments'.format(file_key=file_key),
            params=None,
            json_body={'message': message, 'comment_id': comment_id, 'client_meta': client_meta},
            model=models.Comment,
        )


    def post_comment_reaction(
        self,
        file_key: str,
        comment_id: str,
        *,
        emoji: str,
    ) -> Union["models.PostCommentReactionResponse", dict]:
        """Add a reaction to a comment

        Posts a new comment reaction on a file comment.

        POST /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return self._call(
            'POST',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params=None,
            json_body={'emoji': emoji},
            model=models.PostCommentReactionResponse,
        )


    def post_dev_resources(
        self,
        *,
        dev_resources: list,
    ) -> Union["models.PostDevResourcesResponse", dict]:
        """Create dev resources

        Bulk create dev resources across multiple files.
        Dev resources that are successfully created will show up in the links_created array in the response.

        If there are any dev resources that cannot be created, you may still get a 200 response. These resources will show up in the errors array. Some reasons a dev resource cannot be created include:

        - Resource points to a `file_key` that cannot be found.
        - The node already has the maximum of 10 dev resources.
        - Another dev resource for the node has the same url.

        POST /v1/dev_resources
        """
        return self._call(
            'POST',
            '/v1/dev_resources',
            params=None,
            json_body={'dev_resources': dev_resources},
            model=models.PostDevResourcesResponse,
        )


    def post_variables(
        self,
        file_key: str,
        *,
        variableCollections: Optional[list] = None,
        variableModes: Optional[list] = None,
        variables: Optional[list] = None,
        variableModeValues: Optional[list] = None,
    ) -> Union["models.PostVariablesResponse", dict]:
        """Create/modify/delete variables

        **This API is available to full members of Enterprise orgs with Editor seats.**

        The `POST /v1/files/:file_key/variables` endpoint lets you bulk create, update, and delete variables and variable collections.

        The request body supports the following 4 top-level arrays. Changes from these arrays will be applied in the below order, and within each array, by array order.

        - **variableCollections**: For creating, updating, and deleting variable collections
        - **variableModes**: For creating, updating, and deleting modes within variable collections
          - Each collection can have a maximum of 40 modes
          - Mode names cannot be longer than 40 characters
        ...

        POST /v1/files/{file_key}/variables
        """
        return self._call(
            'POST',
            '/v1/files/{file_key}/variables'.format(file_key=file_key),
            params=None,
            json_body={'variableCollections': variableCollections, 'variableModes': variableModes, 'variables': variables, 'variableModeValues': variableModeValues},
            model=models.PostVariablesResponse,
        )


    def post_webhook(
        self,
        *,
        event_type: str,
        team_id: Optional[str] = None,
        context: str,
        context_id: str,
        endpoint: str,
        passcode: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Union["models.WebhookV2", dict]:
        """Create a webhook

        Create a new webhook which will call the specified endpoint when the event triggers. By default, this webhook will automatically send a PING event to the endpoint when it is created. If this behavior is not desired, you can create the webhook and set the status to PAUSED and reactivate it later.

        POST /v2/webhooks
        """
        return self._call(
            'POST',
            '/v2/webhooks',
            params=None,
            json_body={'event_type': event_type, 'team_id': team_id, 'context': context, 'context_id': context_id, 'endpoint': endpoint, 'passcode': passcode, 'status': status, 'description': description},
            model=models.WebhookV2,
        )


    def put_dev_resources(
        self,
        *,
        dev_resources: list,
    ) -> Union["models.PutDevResourcesResponse", dict]:
        """Update dev resources

        Bulk update dev resources across multiple files.

        Ids for dev resources that are successfully updated will show up in the `links_updated` array in the response.

        If there are any dev resources that cannot be updated, you may still get a 200 response. These resources will show up in the `errors` array.

        PUT /v1/dev_resources
        """
        return self._call(
            'PUT',
            '/v1/dev_resources',
            params=None,
            json_body={'dev_resources': dev_resources},
            model=models.PutDevResourcesResponse,
        )


    def put_webhook(
        self,
        webhook_id: str,
        *,
        event_type: str,
        endpoint: str,
        passcode: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Union["models.WebhookV2", dict]:
        """Update a webhook

        Update a webhook by ID.

        PUT /v2/webhooks/{webhook_id}
        """
        return self._call(
            'PUT',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body={'event_type': event_type, 'endpoint': endpoint, 'passcode': passcode, 'status': status, 'description': description},
            model=models.WebhookV2,
        )




class AsyncEndpoints:

    async def delete_comment(
        self,
        file_key: str,
        comment_id: str,
    ) -> Union["models.DeleteCommentResponse", dict]:
        """Delete a comment

        Deletes a specific comment. Only the person who made the comment is allowed to delete it.

        DELETE /v1/files/{file_key}/comments/{comment_id}
        """
        return await self._call(
            'DELETE',
            '/v1/files/{file_key}/comments/{comment_id}'.format(file_key=file_key, comment_id=comment_id),
            params=None,
            json_body=None,
            model=models.DeleteCommentResponse,
        )


    async def delete_comment_reaction(
        self,
        file_key: str,
        comment_id: str,
        *,
        emoji: str,
    ) -> Union["models.DeleteCommentReactionResponse", dict]:
        """Delete a reaction

        Deletes a specific comment reaction. Only the person who made the reaction is allowed to delete it.

        DELETE /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return await self._call(
            'DELETE',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params={'emoji': emoji},
            json_body=None,
            model=models.DeleteCommentReactionResponse,
        )


    async def delete_dev_resource(
        self,
        file_key: str,
        dev_resource_id: str,
    ) -> Union[Any, dict]:
        """Delete dev resource

        Delete a dev resource from a file

        DELETE /v1/files/{file_key}/dev_resources/{dev_resource_id}
        """
        return await self._call(
            'DELETE',
            '/v1/files/{file_key}/dev_resources/{dev_resource_id}'.format(file_key=file_key, dev_resource_id=dev_resource_id),
            params=None,
            json_body=None,
            model=None,
        )


    async def delete_webhook(
        self,
        webhook_id: str,
    ) -> Union["models.WebhookV2", dict]:
        """Delete a webhook

        Deletes the specified webhook. This operation cannot be reversed.

        DELETE /v2/webhooks/{webhook_id}
        """
        return await self._call(
            'DELETE',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.WebhookV2,
        )


    async def get_activity_logs(
        self,
        *,
        events: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: Optional[float] = None,
        order: Optional[str] = None,
    ) -> Union["models.GetActivityLogsResponse", dict]:
        """Get activity logs

        Returns a list of activity log events

        GET /v1/activity_logs
        """
        return await self._call(
            'GET',
            '/v1/activity_logs',
            params={'events': events, 'start_time': start_time, 'end_time': end_time, 'limit': limit, 'order': order},
            json_body=None,
            model=models.GetActivityLogsResponse,
        )


    async def get_ai_usage_daily(
        self,
        *,
        start_date: str,
        end_date: str,
        user_email: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.GetAiUsageDailyResponse", dict]:
        """Get daily AI credit usage

        Returns per-user, per-day AI credit usage for the plan associated with the calling token. This endpoint requires a plan access token with the `org:ai_metering_usage_read` scope.

        GET /v1/ai_usage/daily
        """
        return await self._call(
            'GET',
            '/v1/ai_usage/daily',
            params={'start_date': start_date, 'end_date': end_date, 'user_email': user_email, 'limit': limit, 'cursor': cursor},
            json_body=None,
            model=models.GetAiUsageDailyResponse,
        )


    async def get_comment_reactions(
        self,
        file_key: str,
        comment_id: str,
        *,
        cursor: Optional[str] = None,
    ) -> Union["models.GetCommentReactionsResponse", dict]:
        """Get reactions for a comment

        Gets a paginated list of reactions left on the comment.

        GET /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params={'cursor': cursor},
            json_body=None,
            model=models.GetCommentReactionsResponse,
        )


    async def get_comments(
        self,
        file_key: str,
        *,
        as_md: Optional[bool] = None,
    ) -> Union["models.GetCommentsResponse", dict]:
        """Get comments in a file

        Gets a list of comments left on the file.

        GET /v1/files/{file_key}/comments
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/comments'.format(file_key=file_key),
            params={'as_md': as_md},
            json_body=None,
            model=models.GetCommentsResponse,
        )


    async def get_component(
        self,
        key: str,
    ) -> Union["models.GetComponentResponse", dict]:
        """Get component

        Get metadata on a component by key.

        GET /v1/components/{key}
        """
        return await self._call(
            'GET',
            '/v1/components/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetComponentResponse,
        )


    async def get_component_set(
        self,
        key: str,
    ) -> Union["models.GetComponentSetResponse", dict]:
        """Get component set

        Get metadata on a published component set by key.

        GET /v1/component_sets/{key}
        """
        return await self._call(
            'GET',
            '/v1/component_sets/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetComponentSetResponse,
        )


    async def get_dev_resources(
        self,
        file_key: str,
        *,
        node_ids: Optional[str] = None,
    ) -> Union["models.GetDevResourcesResponse", dict]:
        """Get dev resources

        Get dev resources in a file

        GET /v1/files/{file_key}/dev_resources
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/dev_resources'.format(file_key=file_key),
            params={'node_ids': node_ids},
            json_body=None,
            model=models.GetDevResourcesResponse,
        )


    async def get_developer_logs(
        self,
        *,
        token_type: Optional[str] = None,
        token: Optional[str] = None,
        token_name: Optional[str] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        event_source: Optional[str] = None,
        date_range: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.PostDeveloperLogsResponse", dict]:
        """Get developer logs

        Returns a list of developer log entries for REST API and MCP server requests made within the organization. This endpoint requires a plan access token with the `org:developer_log_read` scope.

        POST /v1/developer_logs
        """
        return await self._call(
            'POST',
            '/v1/developer_logs',
            params=None,
            json_body={'token_type': token_type, 'token': token, 'token_name': token_name, 'user_email': user_email, 'ip_address': ip_address, 'event_source': event_source, 'date_range': date_range, 'limit': limit, 'cursor': cursor},
            model=models.PostDeveloperLogsResponse,
        )


    async def get_file(
        self,
        file_key: str,
        *,
        version: Optional[str] = None,
        ids: Optional[str] = None,
        depth: Optional[float] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetFileResponse", dict]:
        """Get file JSON

        Returns the document identified by `file_key` as a JSON object. The file key can be parsed from any Figma file url: `https://www.figma.com/file/{file_key}/{title}`.

        The `document` property contains a node of type `DOCUMENT`.

        The `components` property contains a mapping from node IDs to component metadata. This is to help you determine which components each instance comes from.

        GET /v1/files/{file_key}
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}'.format(file_key=file_key),
            params={'version': version, 'ids': ids, 'depth': depth, 'geometry': geometry, 'plugin_data': plugin_data, 'branch_data': branch_data},
            json_body=None,
            model=models.GetFileResponse,
        )


    async def get_file_component_sets(
        self,
        file_key: str,
    ) -> Union["models.GetFileComponentSetsResponse", dict]:
        """Get file component sets

        Get a list of published component sets within a file library.

        GET /v1/files/{file_key}/component_sets
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/component_sets'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileComponentSetsResponse,
        )


    async def get_file_components(
        self,
        file_key: str,
    ) -> Union["models.GetFileComponentsResponse", dict]:
        """Get file components

        Get a list of published components within a file library.

        GET /v1/files/{file_key}/components
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/components'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileComponentsResponse,
        )


    async def get_file_meta(
        self,
        file_key: str,
    ) -> Union["models.GetFileMetaResponse", dict]:
        """Get file metadata

        Get file metadata

        GET /v1/files/{file_key}/meta
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/meta'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileMetaResponse,
        )


    async def get_file_nodes(
        self,
        file_key: str,
        *,
        ids: str,
        version: Optional[str] = None,
        depth: Optional[float] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None,
    ) -> Union["models.GetFileNodesResponse", dict]:
        """Get file JSON for specific nodes

        Returns the nodes referenced to by `ids` as a JSON object. The nodes are retrieved from the Figma file referenced to by `file_key`.

        The node ID and file key can be parsed from any Figma node url: `https://www.figma.com/file/{file_key}/{title}?node-id={id}`

        The `name`, `lastModified`, `thumbnailUrl`, `editorType`, and `version` attributes are all metadata of the specified file.

        ...

        GET /v1/files/{file_key}/nodes
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/nodes'.format(file_key=file_key),
            params={'ids': ids, 'version': version, 'depth': depth, 'geometry': geometry, 'plugin_data': plugin_data},
            json_body=None,
            model=models.GetFileNodesResponse,
        )


    async def get_file_styles(
        self,
        file_key: str,
    ) -> Union["models.GetFileStylesResponse", dict]:
        """Get file styles

        Get a list of published styles within a file library.

        GET /v1/files/{file_key}/styles
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/styles'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetFileStylesResponse,
        )


    async def get_file_versions(
        self,
        file_key: str,
        *,
        page_size: Optional[float] = None,
        before: Optional[float] = None,
        after: Optional[float] = None,
    ) -> Union["models.GetFileVersionsResponse", dict]:
        """Get versions of a file

        This endpoint fetches the version history of a file, allowing you to see the progression of a file over time. You can then use this information to render a specific version of the file, via another endpoint.

        GET /v1/files/{file_key}/versions
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/versions'.format(file_key=file_key),
            params={'page_size': page_size, 'before': before, 'after': after},
            json_body=None,
            model=models.GetFileVersionsResponse,
        )


    async def get_folder_files(
        self,
        folder_id: str,
        *,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetFolderFilesResponse", dict]:
        """Get files in a folder

        Get a list of the files directly within the specified folder.

        GET /v2/folders/{folder_id}/files
        """
        return await self._call(
            'GET',
            '/v2/folders/{folder_id}/files'.format(folder_id=folder_id),
            params={'branch_data': branch_data},
            json_body=None,
            model=models.GetFolderFilesResponse,
        )


    async def get_folder_folders(
        self,
        folder_id: str,
    ) -> Union["models.GetFolderFoldersResponse", dict]:
        """Get subfolders in a folder

        Get a list of the direct subfolders within the specified folder.

        GET /v2/folders/{folder_id}/folders
        """
        return await self._call(
            'GET',
            '/v2/folders/{folder_id}/folders'.format(folder_id=folder_id),
            params=None,
            json_body=None,
            model=models.GetFolderFoldersResponse,
        )


    async def get_folder_meta(
        self,
        folder_id: str,
    ) -> Union["models.GetFolderMetaResponse", dict]:
        """Get folder metadata

        Get metadata for a folder (name, thumbnail, file count, timestamps) without enumerating its files.

        GET /v2/folders/{folder_id}/meta
        """
        return await self._call(
            'GET',
            '/v2/folders/{folder_id}/meta'.format(folder_id=folder_id),
            params=None,
            json_body=None,
            model=models.GetFolderMetaResponse,
        )


    async def get_image_fills(
        self,
        file_key: str,
    ) -> Union["models.GetImageFillsResponse", dict]:
        """Get image fills

        Returns download links for all images present in image fills in a document. Image fills are how Figma represents any user supplied images. When you drag an image into Figma, we create a rectangle with a single fill that represents the image, and the user is able to transform the rectangle (and properties on the fill) as they wish.

        This endpoint returns a mapping from image references to the URLs at which the images may be download. Image URLs will expire after no more than 14 days. Image references are located in the output of the GET files endpoint under the `imageRef` attribute in a `Paint`.

        GET /v1/files/{file_key}/images
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/images'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetImageFillsResponse,
        )


    async def get_images(
        self,
        file_key: str,
        *,
        ids: str,
        version: Optional[str] = None,
        scale: Optional[float] = None,
        format: Optional[str] = None,
        svg_outline_text: Optional[bool] = None,
        svg_include_id: Optional[bool] = None,
        svg_include_node_id: Optional[bool] = None,
        svg_simplify_stroke: Optional[bool] = None,
        contents_only: Optional[bool] = None,
        use_absolute_bounds: Optional[bool] = None,
    ) -> Union["models.GetImagesResponse", dict]:
        """Render images of file nodes

        Renders images from a file.

        If no error occurs, `"images"` will be populated with a map from node IDs to URLs of the rendered images, and `"status"` will be omitted. The image assets will expire after 30 days. Images up to 32 megapixels can be exported. Any images that are larger will be scaled down.

        Important: the image map may contain values that are `null`. This indicates that rendering of that specific node has failed. This may be due to the node id not existing, or other reasons such has the node having no renderable components. It is guaranteed that any node that was requested for rendering will be represented in this map whether or not the render succeeded.

        ...

        GET /v1/images/{file_key}
        """
        return await self._call(
            'GET',
            '/v1/images/{file_key}'.format(file_key=file_key),
            params={'ids': ids, 'version': version, 'scale': scale, 'format': format, 'svg_outline_text': svg_outline_text, 'svg_include_id': svg_include_id, 'svg_include_node_id': svg_include_node_id, 'svg_simplify_stroke': svg_simplify_stroke, 'contents_only': contents_only, 'use_absolute_bounds': use_absolute_bounds},
            json_body=None,
            model=models.GetImagesResponse,
        )


    async def get_library_analytics_component_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsComponentActionsResponse", dict]:
        """Get library analytics component action data.

        Returns a list of library analytics component actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/component/actions
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/component/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsComponentActionsResponse,
        )


    async def get_library_analytics_component_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsComponentUsagesResponse", dict]:
        """Get library analytics component usage data.

        Returns a list of library analytics component usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/component/usages
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/component/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsComponentUsagesResponse,
        )


    async def get_library_analytics_style_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsStyleActionsResponse", dict]:
        """Get library analytics style action data.

        Returns a list of library analytics style actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/style/actions
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/style/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsStyleActionsResponse,
        )


    async def get_library_analytics_style_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsStyleUsagesResponse", dict]:
        """Get library analytics style usage data.

        Returns a list of library analytics style usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/style/usages
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/style/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsStyleUsagesResponse,
        )


    async def get_library_analytics_variable_actions(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Union["models.GetLibraryAnalyticsVariableActionsResponse", dict]:
        """Get library analytics variable action data.

        Returns a list of library analytics variable actions data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/variable/actions
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/variable/actions'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by, 'start_date': start_date, 'end_date': end_date},
            json_body=None,
            model=models.GetLibraryAnalyticsVariableActionsResponse,
        )


    async def get_library_analytics_variable_usages(
        self,
        file_key: str,
        *,
        cursor: Optional[str] = None,
        group_by: str,
    ) -> Union["models.GetLibraryAnalyticsVariableUsagesResponse", dict]:
        """Get library analytics variable usage data.

        Returns a list of library analytics variable usage data broken down by the requested dimension.

        GET /v1/analytics/libraries/{file_key}/variable/usages
        """
        return await self._call(
            'GET',
            '/v1/analytics/libraries/{file_key}/variable/usages'.format(file_key=file_key),
            params={'cursor': cursor, 'group_by': group_by},
            json_body=None,
            model=models.GetLibraryAnalyticsVariableUsagesResponse,
        )


    async def get_local_variables(
        self,
        file_key: str,
    ) -> Union["models.GetLocalVariablesResponse", dict]:
        """Get local variables

        **This API is available to full members of Enterprise orgs.**

        The `GET /v1/files/:file_key/variables/local` endpoint lets you enumerate local variables created in the file and remote variables used in the file. Remote variables are referenced by their `subscribed_id`.

        As a part of the Variables related API additions, the `GET /v1/files/:file_key` endpoint now returns a `boundVariables` property, containing the `variableId` of the bound variable. The `GET /v1/files/:file_key/variables/local` endpoint can be used to get the full variable or variable collection object.

        ...

        GET /v1/files/{file_key}/variables/local
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/variables/local'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetLocalVariablesResponse,
        )


    async def get_me(
        self,
    ) -> Union["models.GetMeResponse", dict]:
        """Get current user

        Returns the user information for the currently authenticated user.

        GET /v1/me
        """
        return await self._call(
            'GET',
            '/v1/me',
            params=None,
            json_body=None,
            model=models.GetMeResponse,
        )


    async def get_o_embed(
        self,
        *,
        url: str,
        maxwidth: Optional[int] = None,
        maxheight: Optional[int] = None,
    ) -> Union["models.GetOEmbedResponse", dict]:
        """Get oEmbed data

        Returns oEmbed data for a Figma file or published Make site URL, following the [oEmbed specification](https://oembed.com/).

        GET /v1/oembed
        """
        return await self._call(
            'GET',
            '/v1/oembed',
            params={'url': url, 'maxwidth': maxwidth, 'maxheight': maxheight},
            json_body=None,
            model=models.GetOEmbedResponse,
        )


    async def get_payments(
        self,
        *,
        plugin_payment_token: Optional[str] = None,
        user_id: Optional[str] = None,
        community_file_id: Optional[str] = None,
        plugin_id: Optional[str] = None,
        widget_id: Optional[str] = None,
    ) -> Union["models.GetPaymentsResponse", dict]:
        """Get payments

        There are two methods to query for a user's payment information on a plugin, widget, or Community file. The first method, using plugin payment tokens, is typically used when making queries from a plugin's or widget's code. The second method, providing a user ID and resource ID, is typically used when making queries from anywhere else.

        Note that you can only query for resources that you own. In most cases, this means that you can only query resources that you originally created.

        GET /v1/payments
        """
        return await self._call(
            'GET',
            '/v1/payments',
            params={'plugin_payment_token': plugin_payment_token, 'user_id': user_id, 'community_file_id': community_file_id, 'plugin_id': plugin_id, 'widget_id': widget_id},
            json_body=None,
            model=models.GetPaymentsResponse,
        )


    async def get_project_files(
        self,
        project_id: str,
        *,
        branch_data: Optional[bool] = None,
    ) -> Union["models.GetProjectFilesResponse", dict]:
        """[Deprecated] Get files in a project

        Deprecated in favor of [Get files in a folder](https://developers.figma.com/docs/rest-api/folders-endpoints/). Get a list of all the Files within the specified project (now called a "folder").

        GET /v1/projects/{project_id}/files
        """
        return await self._call(
            'GET',
            '/v1/projects/{project_id}/files'.format(project_id=project_id),
            params={'branch_data': branch_data},
            json_body=None,
            model=models.GetProjectFilesResponse,
        )


    async def get_project_meta(
        self,
        project_id: str,
    ) -> Union["models.GetProjectMetaResponse", dict]:
        """[Deprecated] Get project metadata

        Deprecated in favor of [Get folder metadata](https://developers.figma.com/docs/rest-api/folders-endpoints/). Get metadata for a project (now called a "folder").

        GET /v1/projects/{project_id}/meta
        """
        return await self._call(
            'GET',
            '/v1/projects/{project_id}/meta'.format(project_id=project_id),
            params=None,
            json_body=None,
            model=models.GetProjectMetaResponse,
        )


    async def get_published_variables(
        self,
        file_key: str,
    ) -> Union["models.GetPublishedVariablesResponse", dict]:
        """Get published variables

        **This API is available to full members of Enterprise orgs.**

        The `GET /v1/files/:file_key/variables/published` endpoint returns the variables that are published from the given file.

        The response for this endpoint contains some key differences compared to the `GET /v1/files/:file_key/variables/local` endpoint:

        - Each variable and variable collection contains a `subscribed_id`.
        - Modes are omitted for published variable collections

        ...

        GET /v1/files/{file_key}/variables/published
        """
        return await self._call(
            'GET',
            '/v1/files/{file_key}/variables/published'.format(file_key=file_key),
            params=None,
            json_body=None,
            model=models.GetPublishedVariablesResponse,
        )


    async def get_style(
        self,
        key: str,
    ) -> Union["models.GetStyleResponse", dict]:
        """Get style

        Get metadata on a style by key.

        GET /v1/styles/{key}
        """
        return await self._call(
            'GET',
            '/v1/styles/{key}'.format(key=key),
            params=None,
            json_body=None,
            model=models.GetStyleResponse,
        )


    async def get_team_component_sets(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamComponentSetsResponse", dict]:
        """Get team component sets

        Get a paginated list of published component sets within a team library.

        GET /v1/teams/{team_id}/component_sets
        """
        return await self._call(
            'GET',
            '/v1/teams/{team_id}/component_sets'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamComponentSetsResponse,
        )


    async def get_team_components(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamComponentsResponse", dict]:
        """Get team components

        Get a paginated list of published components within a team library.

        GET /v1/teams/{team_id}/components
        """
        return await self._call(
            'GET',
            '/v1/teams/{team_id}/components'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamComponentsResponse,
        )


    async def get_team_folders(
        self,
        team_id: str,
    ) -> Union["models.GetTeamFoldersResponse", dict]:
        """Get top-level folders in a team

        Get a list of the top-level folders (previously called "projects") within the specified team. Subfolders can be traversed with the GET /v2/folders/{folder_id}/folders endpoint. It is not possible to programmatically obtain team IDs. To obtain a team ID, navigate to the team page in the Figma file browser. The team ID is present in the URL after the word team. For example, in `https://www.figma.com/files/181033233908053158/team/1535685101263221741`, the team ID is `1535685101263221741`.

        GET /v2/teams/{team_id}/folders
        """
        return await self._call(
            'GET',
            '/v2/teams/{team_id}/folders'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamFoldersResponse,
        )


    async def get_team_projects(
        self,
        team_id: str,
    ) -> Union["models.GetTeamProjectsResponse", dict]:
        """[Deprecated] Get projects in a team

        Deprecated in favor of [Get top-level folders in a team](https://developers.figma.com/docs/rest-api/folders-endpoints/). You can use this endpoint to get a list of the top-level Projects (now called "folders") within the specified team. This will only return projects visible to the authenticated user or owner of the developer token. Note: it is not currently possible to programmatically obtain the team id of a user just from a token. To obtain a team id, navigate to a team page of a team you are a part of. The team id will be present in the URL after the word team and before your team name.

        GET /v1/teams/{team_id}/projects
        """
        return await self._call(
            'GET',
            '/v1/teams/{team_id}/projects'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamProjectsResponse,
        )


    async def get_team_styles(
        self,
        team_id: str,
        *,
        page_size: Optional[float] = None,
        after: Optional[float] = None,
        before: Optional[float] = None,
    ) -> Union["models.GetTeamStylesResponse", dict]:
        """Get team styles

        Get a paginated list of published styles within a team library.

        GET /v1/teams/{team_id}/styles
        """
        return await self._call(
            'GET',
            '/v1/teams/{team_id}/styles'.format(team_id=team_id),
            params={'page_size': page_size, 'after': after, 'before': before},
            json_body=None,
            model=models.GetTeamStylesResponse,
        )


    async def get_team_webhooks(
        self,
        team_id: str,
    ) -> Union["models.GetTeamWebhooksResponse", dict]:
        """[Deprecated] Get team webhooks

        Returns all webhooks registered under the specified team.

        GET /v2/teams/{team_id}/webhooks
        """
        return await self._call(
            'GET',
            '/v2/teams/{team_id}/webhooks'.format(team_id=team_id),
            params=None,
            json_body=None,
            model=models.GetTeamWebhooksResponse,
        )


    async def get_webhook(
        self,
        webhook_id: str,
    ) -> Union["models.WebhookV2", dict]:
        """Get a webhook

        Get a webhook by ID.

        GET /v2/webhooks/{webhook_id}
        """
        return await self._call(
            'GET',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.WebhookV2,
        )


    async def get_webhook_requests(
        self,
        webhook_id: str,
    ) -> Union["models.GetWebhookRequestsResponse", dict]:
        """Get webhook requests

        Returns all webhook requests sent within the last week. Useful for debugging.

        GET /v2/webhooks/{webhook_id}/requests
        """
        return await self._call(
            'GET',
            '/v2/webhooks/{webhook_id}/requests'.format(webhook_id=webhook_id),
            params=None,
            json_body=None,
            model=models.GetWebhookRequestsResponse,
        )


    async def get_webhooks(
        self,
        *,
        context: Optional[str] = None,
        context_id: Optional[str] = None,
        plan_api_id: Optional[str] = None,
        cursor: Optional[str] = None,
    ) -> Union["models.GetWebhooksResponse", dict]:
        """Get webhooks by context or plan

        Returns a list of webhooks corresponding to the context or plan provided, if they exist. For plan, the webhooks for all contexts that you have access to will be returned, and theresponse is paginated

        GET /v2/webhooks
        """
        return await self._call(
            'GET',
            '/v2/webhooks',
            params={'context': context, 'context_id': context_id, 'plan_api_id': plan_api_id, 'cursor': cursor},
            json_body=None,
            model=models.GetWebhooksResponse,
        )


    async def post_comment(
        self,
        file_key: str,
        *,
        message: str,
        comment_id: Optional[str] = None,
        client_meta: Optional[Any] = None,
    ) -> Union["models.Comment", dict]:
        """Add a comment to a file

        Posts a new comment on the file.

        POST /v1/files/{file_key}/comments
        """
        return await self._call(
            'POST',
            '/v1/files/{file_key}/comments'.format(file_key=file_key),
            params=None,
            json_body={'message': message, 'comment_id': comment_id, 'client_meta': client_meta},
            model=models.Comment,
        )


    async def post_comment_reaction(
        self,
        file_key: str,
        comment_id: str,
        *,
        emoji: str,
    ) -> Union["models.PostCommentReactionResponse", dict]:
        """Add a reaction to a comment

        Posts a new comment reaction on a file comment.

        POST /v1/files/{file_key}/comments/{comment_id}/reactions
        """
        return await self._call(
            'POST',
            '/v1/files/{file_key}/comments/{comment_id}/reactions'.format(file_key=file_key, comment_id=comment_id),
            params=None,
            json_body={'emoji': emoji},
            model=models.PostCommentReactionResponse,
        )


    async def post_dev_resources(
        self,
        *,
        dev_resources: list,
    ) -> Union["models.PostDevResourcesResponse", dict]:
        """Create dev resources

        Bulk create dev resources across multiple files.
        Dev resources that are successfully created will show up in the links_created array in the response.

        If there are any dev resources that cannot be created, you may still get a 200 response. These resources will show up in the errors array. Some reasons a dev resource cannot be created include:

        - Resource points to a `file_key` that cannot be found.
        - The node already has the maximum of 10 dev resources.
        - Another dev resource for the node has the same url.

        POST /v1/dev_resources
        """
        return await self._call(
            'POST',
            '/v1/dev_resources',
            params=None,
            json_body={'dev_resources': dev_resources},
            model=models.PostDevResourcesResponse,
        )


    async def post_variables(
        self,
        file_key: str,
        *,
        variableCollections: Optional[list] = None,
        variableModes: Optional[list] = None,
        variables: Optional[list] = None,
        variableModeValues: Optional[list] = None,
    ) -> Union["models.PostVariablesResponse", dict]:
        """Create/modify/delete variables

        **This API is available to full members of Enterprise orgs with Editor seats.**

        The `POST /v1/files/:file_key/variables` endpoint lets you bulk create, update, and delete variables and variable collections.

        The request body supports the following 4 top-level arrays. Changes from these arrays will be applied in the below order, and within each array, by array order.

        - **variableCollections**: For creating, updating, and deleting variable collections
        - **variableModes**: For creating, updating, and deleting modes within variable collections
          - Each collection can have a maximum of 40 modes
          - Mode names cannot be longer than 40 characters
        ...

        POST /v1/files/{file_key}/variables
        """
        return await self._call(
            'POST',
            '/v1/files/{file_key}/variables'.format(file_key=file_key),
            params=None,
            json_body={'variableCollections': variableCollections, 'variableModes': variableModes, 'variables': variables, 'variableModeValues': variableModeValues},
            model=models.PostVariablesResponse,
        )


    async def post_webhook(
        self,
        *,
        event_type: str,
        team_id: Optional[str] = None,
        context: str,
        context_id: str,
        endpoint: str,
        passcode: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Union["models.WebhookV2", dict]:
        """Create a webhook

        Create a new webhook which will call the specified endpoint when the event triggers. By default, this webhook will automatically send a PING event to the endpoint when it is created. If this behavior is not desired, you can create the webhook and set the status to PAUSED and reactivate it later.

        POST /v2/webhooks
        """
        return await self._call(
            'POST',
            '/v2/webhooks',
            params=None,
            json_body={'event_type': event_type, 'team_id': team_id, 'context': context, 'context_id': context_id, 'endpoint': endpoint, 'passcode': passcode, 'status': status, 'description': description},
            model=models.WebhookV2,
        )


    async def put_dev_resources(
        self,
        *,
        dev_resources: list,
    ) -> Union["models.PutDevResourcesResponse", dict]:
        """Update dev resources

        Bulk update dev resources across multiple files.

        Ids for dev resources that are successfully updated will show up in the `links_updated` array in the response.

        If there are any dev resources that cannot be updated, you may still get a 200 response. These resources will show up in the `errors` array.

        PUT /v1/dev_resources
        """
        return await self._call(
            'PUT',
            '/v1/dev_resources',
            params=None,
            json_body={'dev_resources': dev_resources},
            model=models.PutDevResourcesResponse,
        )


    async def put_webhook(
        self,
        webhook_id: str,
        *,
        event_type: str,
        endpoint: str,
        passcode: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Union["models.WebhookV2", dict]:
        """Update a webhook

        Update a webhook by ID.

        PUT /v2/webhooks/{webhook_id}
        """
        return await self._call(
            'PUT',
            '/v2/webhooks/{webhook_id}'.format(webhook_id=webhook_id),
            params=None,
            json_body={'event_type': event_type, 'endpoint': endpoint, 'passcode': passcode, 'status': status, 'description': description},
            model=models.WebhookV2,
        )
