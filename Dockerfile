# We're using Ubuntu 20.10
FROM alfianandaa/alf:groovy

RUN mkdir /xnewbie && chmod 777 /xnewbie
ENV PATH="/xnewbie/bin:$PATH"
WORKDIR /xnewbie

RUN git clone https://github.com/X-Newbie/XBot-Remix -b sql-extended /xnewbie

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/X-Newbie/XUserbot/sql-extended/requirements.txt

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /xnewbie/

#
# Make open port TCP
#
EXPOSE 80 443

#
# Finalization
#
CMD ["python3","-m","userbot"]
