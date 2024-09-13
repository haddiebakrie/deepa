from database.operations import DBOperations
from database.decorators import db_error_handler, failSilent, failNoise

class DBSchema(DBOperations):

    def initializeSchema(self):
        with self.connect() as conn:
            self.createUserSchema(conn)
            self.createStoreSchema(conn)
            self.createShippingSchema(conn)
            self.createProductSchema(conn)
            self.createTransactionSchema(conn)
            self.createPaymentSchema(conn)
            self.createDeepaLogSchema(conn)
            self.createMerchantLogSchema(conn)
            self.createUserLogSchema(conn)
            self.createContractSchema(conn)
            conn.commit()

    @db_error_handler
    def createUserSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""   
                CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                userID VARCHAR UNIQUE,
                phone VARCHAR UNIQUE NOT NULL,
                username VARCHAR UNIQUE,
                passwordHash TEXT,
                isVerified bool DEFAULT false,
                status VARCHAR NOT NULL DEFAULT 'active',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                lastLogin TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata jsonb
                );

            """)

    @db_error_handler
    def createShippingSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""      
                CREATE TABLE IF NOT EXISTS "shippingLocation" (
                id SERIAL PRIMARY KEY,
                shippingLocationID VARCHAR UNIQUE,
                state VARCHAR NOT NULL,
                cities jsonb,
                shippingNote VARCHAR,
                shippingDuration INTEGER NOT NULL,
                shippingAmount DOUBLE PRECISION NOT NULL,
                storeID INTEGER REFERENCES "store" (id) ON DELETE CASCADE,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );
                           
                CREATE TABLE IF NOT EXISTS "shipping" (
                id SERIAL PRIMARY KEY,
                shippingTitle VARCHAR,
                shippingID VARCHAR UNIQUE,
                shippingDescription VARCHAR,
                shippingStatus VARCHAR DEFAULT 'pending',
                shippingLocationID INTEGER REFERENCES "shippingLocation" (id),
                contractID INTEGER REFERENCES "contract" (id) ON DELETE CASCADE,
                buyerID INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );

            """)

    @db_error_handler
    def createProductSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "product" (
                id SERIAL PRIMARY KEY,
                productTitle VARCHAR,
                productAmount DOUBLE PRECISION,
                productDescription TEXT,
                paidAmount DOUBLE PRECISION DEFAULT 0.0,
                productID VARCHAR UNIQUE,
                userID INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
                storeID VARCHAR REFERENCES "store" (storeID) ON DELETE CASCADE,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );
                           
                CREATE TABLE IF NOT EXISTS "productHandle" (
                id SERIAL PRIMARY KEY,
                productID INTEGER REFERENCES "product" (id) ON DELETE CASCADE,
                productLink VARCHAR UNIQUE,
                productDeepaLink VARCHAR UNIQUE,
                productHandle VARCHAR UNIQUE
                );
                           
                -- CREATE INDEX product_note_idx ON product USING GIN (to_tsvector(productDescription));
                -- CREATE INDEX product_title_idx ON product USING GIN (to_tsvector(productTitle));
                           
            """)

    @db_error_handler
    def createStoreSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "store" (
                id SERIAL PRIMARY KEY,
                handle VARCHAR UNIQUE,
                storeID VARCHAR UNIQUE,
                storeDescription TEXT,
                storeTitle TEXT,
                userID INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );
                                  
            """)


    @db_error_handler
    def createContractSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
                cursor.execute("""
                                               
                -- CREATE TYPE fulfillmentStatusEnum AS ENUM
                -- ('pending', 'active', 'partiallyFulfilled', 'fulfilled', 
                -- 'partiallyShipped', 'shipped', 'partiallyReturned', 
                -- 'returned', 'cancelled', 'requiresAction');
                
                CREATE TABLE IF NOT EXISTS "contract" (
                id SERIAL PRIMARY KEY,
                contractTitle VARCHAR,
                contractID VARCHAR UNIQUE,
                sellerID VARCHAR REFERENCES "store" (storeID),
                buyerID INTEGER REFERENCES "user" (id),
                productID INTEGER REFERENCES "product" (id),
                fulfillmentStatus VARCHAR NOT NULL DEFAULT 'pending',
                contractDescription TEXT,
                paidAmount DOUBLE PRECISION DEFAULT 0,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );
                               
                -- CREATE INDEX contract_note_idx ON contract USING GIN (to_tsvector(note));
                -- CREATE INDEX contract_title_idx ON contract USING GIN (to_tsvector(contractTitle));

            """)

    @db_error_handler
    def createPaymentSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "payment" (
                id SERIAL PRIMARY KEY,
                paymentID VARCHAR UNIQUE,
                contractID INTEGER REFERENCES "contract" (id),
                amount DOUBLE PRECISION,
                createdAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deletedAt timestamp with time zone,
                metadata jsonb
                );
                           
            """)

    @db_error_handler
    def createTransactionSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                            
                CREATE TABLE IF NOT EXISTS "payment" (
                id SERIAL PRIMARY KEY,
                type VARCHAR,
                payable bool DEFAULT false,
                note TEXT,
                metadata jsonb
                );
                           
            """)
            
    @db_error_handler
    def createDeepaLogSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                            
                CREATE TABLE IF NOT EXISTS "logs" (
                id SERIAL PRIMARY KEY,
                transaction_id INTEGER REFERENCES "transaction",
                metadata jsonb
                );
            """)
            
    @db_error_handler
    def createMerchantLogSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                            
                CREATE TABLE IF NOT EXISTS "merchantLog" (
                id SERIAL PRIMARY KEY,
                metadata jsonb
                );
            """)
            
    @db_error_handler
    def createUserLogSchema(self, conn):
        conn.commit() # Ensure last transaction is aborted if it fails
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "notification" (
                id SERIAL PRIMARY KEY,
                metadata jsonb
                );
            """)


    def runTest(self):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO "transaction"
                (note)
                VALUES(%s)
                """, ("NGN 100 Airtime recharge for Timmy", )
            )
            cur.execute(
                """
                SELECT * FROM "transaction"
                WHERE to_tsvector(note) @@ to_tsquery('airtime & timmy & 100');
                """
            ) 
            print(cur.fetchall())
            conn.commit()
            
    

if __name__ == "__main__":
     db = DBSchema()
     db.initializeSchema()
     db.runTest()