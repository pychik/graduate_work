from notify.dataclasses import DataModel, UserData
from notify.handlers.base import BaseHandler
from notify.utils import get_rendered_template


class LikesHandler(BaseHandler):
    template_name = 'like.html'
    subject = 'Your comment is popular!'

    def prepare_data(self):
        data = self.nl.notification_data

        comment_link = data.pop('link')
        likes_count = data.pop('count')

        user_list = [UserData(**data)]

        first_name = data.get('first_name')

        values_to_render = dict(first_name=first_name, comment_link=comment_link, likes_count=likes_count)
        template = get_rendered_template(self.template_name, values_to_render)
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return DataModel(**data_to_send)
        except Exception as e:
            self.nl.log_error(e)
            raise e
