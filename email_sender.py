import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, RECIPIENT_EMAILS
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_purdue_theme_html(content: str) -> str:
    """Create HTML email with Purdue theme (gold and black colors) with card-based layout."""
    import html
    
    def escape_html(text):
        """Escape HTML special characters."""
        return html.escape(text)
    
    # Parse content into structured sections
    sections = []
    current_section = {'title': None, 'content': [], 'insight': None, 'action': None}
    in_key_takeaways = False
    key_takeaways = []
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip() if lines[i] else ''
        
        # Check for Key Takeaways section
        if '**Key takeaways:**' in line or 'Key takeaways:' in line:
            in_key_takeaways = True
            # Extract text after the label
            if ':' in line:
                remainder = line.split(':', 1)[1].strip()
                if remainder:
                    key_takeaways.append(remainder)
            i += 1
            continue
        
        if in_key_takeaways:
            if line:
                key_takeaways.append(line)
            i += 1
            continue
        
        # Check for story title (starts with **)
        if line.startswith('**') and line.endswith('**') and len(line) > 4:
            # Save previous section if it exists
            if current_section['title']:
                sections.append(current_section.copy())
            # Start new section
            title = line.strip('*').strip()
            current_section = {
                'title': title,
                'content': [],
                'insight': None,
                'action': None
            }
            i += 1
            continue
        
        # Check for Strategic insight
        if line.startswith('Strategic insight:'):
            current_section['insight'] = line.replace('Strategic insight:', '').strip()
            i += 1
            continue
        
        # Check for Your move
        if line.startswith('Your move:'):
            current_section['action'] = line.replace('Your move:', '').strip()
            i += 1
            continue
        
        # Regular content
        if line and current_section['title']:
            current_section['content'].append(line)
        
        i += 1
    
    # Add last section
    if current_section['title']:
        sections.append(current_section)
    
    # Build HTML for story cards
    story_cards_html = ''
    
    # If no sections were parsed, create a fallback card with all content
    if not sections:
        escaped_content = escape_html(content)
        # Convert newlines to <br> and paragraphs
        formatted_content = escaped_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
        story_cards_html = f'''
        <div class="story-card">
            <div class="story-content">
                <p>{formatted_content}</p>
            </div>
        </div>
        '''
    
    for section in sections:
        # Escape and format content paragraphs
        content_paragraphs = []
        for p in section['content']:
            if p.strip():
                escaped = escape_html(p.strip())
                content_paragraphs.append(f'<p style="margin: 0 0 12px 0; line-height: 1.7;">{escaped}</p>')
        content_html = ''.join(content_paragraphs)
        
        insight_html = ''
        if section['insight']:
            escaped_insight = escape_html(section['insight'])
            insight_html = f'''
            <div class="insight-box">
                <div class="insight-label">Strategic insight</div>
                <div class="insight-content">{escaped_insight}</div>
            </div>
            '''
        
        action_html = ''
        if section['action']:
            escaped_action = escape_html(section['action'])
            action_html = f'''
            <div class="action-box">
                <div class="action-label">Your move</div>
                <div class="action-content">{escaped_action}</div>
            </div>
            '''
        
        escaped_title = escape_html(section['title'])
        story_cards_html += f'''
        <div class="story-card">
            <h2 class="story-title">{escaped_title}</h2>
            <div class="story-content">
                {content_html}
            </div>
            {insight_html}
            {action_html}
        </div>
        '''
    
    # Build key takeaways section
    takeaways_html = ''
    if key_takeaways:
        takeaways_text = ' '.join(key_takeaways)
        # Remove markdown bold markers (**)
        takeaways_text = takeaways_text.replace('**', '')
        escaped_takeaways = escape_html(takeaways_text)
        # Use solid background color for Outlook compatibility (Outlook doesn't support gradients well)
        takeaways_html = f'''
        <div class="takeaways-card" style="background-color: #FFF9E6 !important; border: 2px solid #CEB888; border-radius: 12px; padding: 28px; margin-top: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h3 class="takeaways-title" style="color: #8B6914 !important; font-size: 20px; font-weight: 700; margin: 0 0 16px 0; text-align: center;">Key Takeaways</h3>
            <p class="takeaways-content" style="color: #000000 !important; font-size: 16px; line-height: 1.7; text-align: center; margin: 0;">{escaped_takeaways}</p>
        </div>
        '''
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #1C1C1C;
                background-color: #f5f5f5;
                padding: 20px;
            }}
            .email-wrapper {{
                max-width: 700px;
                margin: 0 auto;
                background-color: #ffffff;
            }}
            .container {{
                background-color: #ffffff;
                padding: 0;
            }}
            .header {{
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #ffffff;
                padding: 40px 40px 30px 40px;
                text-align: center;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            .header h1 {{
                color: #CEB888;
                margin: 0 0 8px 0;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header .subtitle {{
                color: #CEB888;
                font-size: 15px;
                margin-top: 5px;
                font-weight: 500;
            }}
            .stories-container {{
                padding: 30px 40px;
            }}
            .story-card {{
                background-color: #ffffff;
                border: 1px solid #e8e8e8;
                border-radius: 12px;
                padding: 28px;
                margin-bottom: 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                transition: box-shadow 0.3s ease;
            }}
            .story-card:hover {{
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            }}
            .story-title {{
                color: #000000;
                font-size: 22px;
                font-weight: 700;
                margin: 0 0 16px 0;
                line-height: 1.3;
                padding-bottom: 12px;
                border-bottom: 2px solid #CEB888;
            }}
            .story-content {{
                color: #333333;
                font-size: 16px;
                line-height: 1.7;
                margin-bottom: 20px;
            }}
            .story-content p {{
                margin: 0 0 12px 0;
            }}
            .insight-box {{
                background: linear-gradient(135deg, #FFF9E6 0%, #FFF5D6 100%);
                border-left: 4px solid #CEB888;
                border-radius: 6px;
                padding: 18px 20px;
                margin: 20px 0;
            }}
            .insight-label {{
                color: #8B6914;
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
            }}
            .insight-content {{
                color: #1C1C1C;
                font-size: 15px;
                line-height: 1.6;
                font-style: italic;
            }}
            .action-box {{
                background: linear-gradient(135deg, #F0F7FF 0%, #E6F2FF 100%);
                border-left: 4px solid #4A90E2;
                border-radius: 6px;
                padding: 18px 20px;
                margin: 20px 0;
            }}
            .action-label {{
                color: #2E5C8A;
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
            }}
            .action-content {{
                color: #1C1C1C;
                font-size: 15px;
                line-height: 1.6;
            }}
            .takeaways-card {{
                background: linear-gradient(135deg, #FFF9E6 0%, #FFF5D6 100%);
                border: 2px solid #CEB888;
                border-radius: 12px;
                padding: 28px;
                margin-top: 32px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .takeaways-title {{
                color: #8B6914;
                font-size: 20px;
                font-weight: 700;
                margin: 0 0 16px 0;
                text-align: center;
            }}
            .takeaways-content {{
                color: #000000;
                font-size: 16px;
                line-height: 1.7;
                text-align: center;
            }}
            .footer {{
                background-color: #fafafa;
                padding: 24px 40px;
                border-top: 1px solid #e8e8e8;
                font-size: 12px;
                color: #666;
                text-align: center;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            .footer p {{
                margin: 4px 0;
            }}
            @media only screen and (max-width: 600px) {{
                .header, .stories-container, .footer {{
                    padding: 24px 20px;
                }}
                .story-card {{
                    padding: 20px;
                }}
                .header h1 {{
                    font-size: 26px;
                }}
                .story-title {{
                    font-size: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="container">
                <div class="header">
                    <h1>MBT Newsletter</h1>
                    <div class="subtitle" style="color: #CEB888 !important; font-size: 15px; margin-top: 5px; font-weight: 500;">Tech & Business Insights for Ambitious Students</div>
                </div>
                <div class="stories-container">
                    {story_cards_html}
                    {takeaways_html}
                </div>
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
                    <p>Stay ahead of the curve.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email(newsletter_content: str, subject: str = "Your MBT Newsletter"):
    """Send newsletter via email to multiple recipients."""
    if not EMAIL_PASSWORD:
        raise ValueError("EMAIL_PASSWORD not set in environment variables")
    
    if not RECIPIENT_EMAILS:
        raise ValueError("No recipient emails configured")
    
    # Create HTML version
    html_content = create_purdue_theme_html(newsletter_content)
    
    try:
        logger.info(f"Sending email to {len(RECIPIENT_EMAILS)} recipient(s): {', '.join(RECIPIENT_EMAILS)}...")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            # Send to each recipient
            for recipient in RECIPIENT_EMAILS:
                # Create message for each recipient
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = recipient
                
                # Attach HTML version
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                
                # Attach plain text version
                text_part = MIMEText(newsletter_content, 'plain')
                msg.attach(text_part)
                
                # Send email
                server.send_message(msg)
                logger.info(f"Email sent successfully to {recipient}")
        
        logger.info(f"All emails sent successfully to {len(RECIPIENT_EMAILS)} recipient(s)")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise

