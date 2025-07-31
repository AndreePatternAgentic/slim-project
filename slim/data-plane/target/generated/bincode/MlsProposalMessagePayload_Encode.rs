impl :: bincode :: Encode for MlsProposalMessagePayload
{
    fn encode < __E : :: bincode :: enc :: Encoder >
    (& self, encoder : & mut __E) ->core :: result :: Result < (), :: bincode
    :: error :: EncodeError >
    {
        :: bincode :: Encode :: encode(&self.source_name, encoder) ?; ::
        bincode :: Encode :: encode(&self.mls_msg, encoder) ?; core :: result
        :: Result :: Ok(())
    }
}