import logging

#################### Set up logging ####################
def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Output logs to console (visible in Streamlit)
            logging.FileHandler('app.log')  # Save logs to a file
        ]
    )
    logger = logging.getLogger(__name__)
    
    return logger